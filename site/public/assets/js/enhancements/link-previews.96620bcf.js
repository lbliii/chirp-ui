(function(){'use strict';function getConfig(){const el=document.getElementById('bengal-config');if(el){try{const cfg=JSON.parse(el.textContent);if(cfg?.linkPreviews){return cfg.linkPreviews;}}catch(err){console.warn('[LinkPreviews] Failed to parse config bridge:',err);}}
const dataEnabled=document.documentElement.dataset.linkPreviews||document.body?.dataset.linkPreviews;if(dataEnabled==='false'){return{enabled:false};}
return{enabled:true};}
const userConfig=getConfig();if(userConfig.enabled===false){return;}
const CONFIG={debug:userConfig.debug??(window.Bengal?.debug)??false,hoverDelay:userConfig.hoverDelay??200,hideDelay:userConfig.hideDelay??150,prefetchDelay:50,maxCacheSize:50,maxExcerptLength:200,previewWidth:320,longPressDelay:500,showSection:userConfig.showSection??true,showReadingTime:userConfig.showReadingTime??true,showWordCount:userConfig.showWordCount??true,showDate:userConfig.showDate??true,showTags:userConfig.showTags??true,maxTags:userConfig.maxTags??3,includeSelectors:userConfig.includeSelectors??['.prose','.content','article','main'],excludeSelectors:userConfig.excludeSelectors??['nav','.toc','.breadcrumb','.pagination','.card',"[class*='-card']",'.tab-nav',"[class*='-widget']",'.child-items','.content-tiles'],allowedHosts:userConfig.allowedHosts??[],allowedSchemes:userConfig.allowedSchemes??['https'],hostFailureThreshold:userConfig.hostFailureThreshold??3,showDeadLinks:userConfig.showDeadLinks??true,};const cache=new Map();let activePreview=null;let activeLink=null;let hoverTimeout=null;let hideTimeout=null;let prefetchTimeout=null;let pendingFetch=null;let jsonAvailable=null;let touchTimeout=null;let touchStartTime=0;let touchStartPos={x:0,y:0};const hostFailures=new Map();const disabledHosts=new Set();function toJsonUrl(pageUrl){if(pageUrl.endsWith('.html')){return pageUrl.replace(/\.html$/,'.json');}
let url=pageUrl.replace(/\/$/,'');if(!url||url===''){return'/index.json';}
return url+'/index.json';}
function isCrossOrigin(link){return link.hostname!==window.location.hostname;}
function isAllowedCrossOrigin(link){const isAllowedHost=CONFIG.allowedHosts.includes(link.hostname);if(!isAllowedHost)return false;const scheme=link.protocol.replace(':','');const isAllowedScheme=CONFIG.allowedSchemes.includes(scheme);if(!isAllowedScheme)return false;if(disabledHosts.has(link.hostname))return false;return true;}
function isPreviewable(link){if(jsonAvailable===false&&!isCrossOrigin(link))return false;const isSameHost=!isCrossOrigin(link);if(!isSameHost&&!isAllowedCrossOrigin(link))return false;if(link.hash&&link.pathname===window.location.pathname)return false;if(link.hasAttribute('download'))return false;if(link.dataset.noPreview!==undefined)return false;if(link.closest('.link-preview'))return false;const includeSelector=CONFIG.includeSelectors.join(', ');if(includeSelector&&!link.closest(includeSelector))return false;const excludeSelector=CONFIG.excludeSelectors.join(', ');if(excludeSelector&&link.closest(excludeSelector))return false;if(link.classList.contains('btn')||link.classList.contains('button')||link.className.includes('btn-')||link.className.includes('button-')||link.getAttribute('role')==='button'){return false;}
if(link.classList.contains('card')||link.className.includes('-card')||link.closest('.card-link, .card-body > a:only-child')){return false;}
if(link.querySelector('svg, img, .icon, [class*="icon"]')){return false;}
const linkText=link.textContent.trim();if(linkText.startsWith('http://')||linkText.startsWith('https://')||linkText.startsWith('www.')){return false;}
if(!linkText||linkText.length<2){return false;}
return true;}
function cacheSet(key,value){if(cache.size>=CONFIG.maxCacheSize){const firstKey=cache.keys().next().value;cache.delete(firstKey);}
cache.set(key,value);}
function generateId(){return'link-preview-'+Math.random().toString(36).slice(2,9);}
function escapeHtml(text){const div=document.createElement('div');div.textContent=text;return div.innerHTML;}
function recordHostFailure(host){const count=(hostFailures.get(host)||0)+1;hostFailures.set(host,count);if(count>=CONFIG.hostFailureThreshold){disabledHosts.add(host);console.info(`[LinkPreviews]Host ${host}disabled after ${count}consecutive failures`);}}
function clearHostFailures(host){hostFailures.delete(host);}
async function fetchPreviewData(url,link){const isCross=link&&isCrossOrigin(link);const cacheKey=isCross?link.href:url;if(cache.has(cacheKey)){return cache.get(cacheKey);}
if(link&&disabledHosts.has(link.hostname)){return null;}
if(pendingFetch&&pendingFetch.url!==cacheKey){pendingFetch.controller.abort();}
const controller=new AbortController();pendingFetch={url:cacheKey,controller};try{let jsonUrl;if(isCross){jsonUrl=toJsonUrl(link.href);}else{jsonUrl=toJsonUrl(url);}
if(CONFIG.debug)console.log('[LinkPreviews] Fetching:',jsonUrl,isCross?'(cross-origin)':'');const fetchOptions={signal:controller.signal};if(isCross){fetchOptions.credentials='omit';fetchOptions.mode='cors';}
const response=await fetch(jsonUrl,fetchOptions);if(!response.ok){if(isCross){recordHostFailure(link.hostname);}
if(response.status===404&&!isCross&&jsonAvailable===null){console.info('[LinkPreviews] JSON files not available, feature disabled');jsonAvailable=false;return null;}
throw new Error(`HTTP ${response.status}`);}
if(!isCross&&jsonAvailable===null){jsonAvailable=true;if(CONFIG.debug)console.log('[LinkPreviews] JSON files detected, feature active');}
if(isCross){clearHostFailures(link.hostname);}
let data=await response.json();if(data.site&&data.pages&&!data.title){const homepage=data.pages.find(p=>p.uri==='/'||p.objectID==='/');if(homepage){data=homepage;}else{data={title:data.site.title||'Untitled',excerpt:data.site.description||'',section:null,tags:[],reading_time:null,word_count:null,date:null,_isSiteIndex:true,};}}
cacheSet(cacheKey,data);pendingFetch=null;return data;}catch(error){pendingFetch=null;if(error.name==='AbortError')return null;if(isCross&&link){recordHostFailure(link.hostname);}
if(CONFIG.debug){console.warn('[LinkPreviews] Fetch failed:',cacheKey,error.message);}
if(CONFIG.showDeadLinks&&!isCross){const deadLinkData={_dead:true,_url:cacheKey,_error:error.message};cacheSet(cacheKey,deadLinkData);return deadLinkData;}
cacheSet(cacheKey,null);return null;}}
function prefetch(link){const cacheKey=isCrossOrigin(link)?link.href:link.pathname;if(cache.has(cacheKey))return;clearTimeout(prefetchTimeout);prefetchTimeout=setTimeout(()=>{fetchPreviewData(link.pathname,link);},CONFIG.prefetchDelay);}
function createPreviewCard(data,link){if(!data)return null;if(activePreview&&activeLink===link)return activePreview;if(data._dead){return createDeadLinkCard(data,link);}
const preview=document.createElement('div');preview.className='link-preview';preview.id=generateId();preview.setAttribute('role','tooltip');link.setAttribute('aria-describedby',preview.id);let html='';if(CONFIG.showSection&&data.section){html+=`<div class="link-preview__section">${escapeHtml(data.section)}</div>`;}
html+=`<h4 class="link-preview__title">${escapeHtml(data.title||'Untitled')}</h4>`;const excerpt=data.excerpt||data.description||'';if(excerpt){html+=`<p class="link-preview__excerpt">${escapeHtml(excerpt)}</p>`;}
const metaParts=[];if(CONFIG.showReadingTime&&data.reading_time){metaParts.push(`<span class="link-preview__meta-item">${data.reading_time}min read</span>`);}
if(CONFIG.showWordCount&&data.word_count){const formatted=data.word_count>=1000?`${(data.word_count/1000).toFixed(1)}k`:data.word_count;metaParts.push(`<span class="link-preview__meta-item">${formatted}words</span>`);}
if(CONFIG.showDate&&data.date){const date=new Date(data.date);const formatted=date.toLocaleDateString(undefined,{month:'short',day:'numeric',year:'numeric'});metaParts.push(`<span class="link-preview__meta-item">${formatted}</span>`);}
if(metaParts.length>0){html+=`<div class="link-preview__meta">${metaParts.join(' · ')}</div>`;}
if(CONFIG.showTags&&data.tags&&data.tags.length>0){const tagsHtml=data.tags.slice(0,CONFIG.maxTags).map(tag=>`<span class="link-preview__tag">${escapeHtml(tag)}</span>`).join('');html+=`<div class="link-preview__tags">${tagsHtml}</div>`;}
preview.innerHTML=html;document.body.appendChild(preview);positionPreview(link,preview);preview.addEventListener('pointerenter',cancelHide);preview.addEventListener('pointerleave',scheduleHide);return preview;}
function createDeadLinkCard(data,link){const preview=document.createElement('div');preview.className='link-preview link-preview--dead';preview.id=generateId();preview.setAttribute('role','tooltip');link.setAttribute('aria-describedby',preview.id);const linkPath=link.pathname||data._url||'Unknown';let html=`<div class="link-preview__dead-icon"aria-hidden="true"><svg width="24"height="24"viewBox="0 0 24 24"fill="none"stroke="currentColor"stroke-width="2"stroke-linecap="round"stroke-linejoin="round"><circle cx="12"cy="12"r="10"></circle><line x1="12"y1="8"x2="12"y2="12"></line><line x1="12"y1="16"x2="12.01"y2="16"></line></svg></div><h4 class="link-preview__title link-preview__title--dead">Page Not Found</h4><p class="link-preview__excerpt link-preview__excerpt--dead">This link may be broken or the page may have moved.</p><div class="link-preview__dead-path"><code>${escapeHtml(linkPath)}</code></div>`;preview.innerHTML=html;document.body.appendChild(preview);positionPreview(link,preview);preview.addEventListener('pointerenter',cancelHide);preview.addEventListener('pointerleave',scheduleHide);return preview;}
function positionPreview(link,preview){const linkRect=link.getBoundingClientRect();const previewRect=preview.getBoundingClientRect();const margin=8;const scrollY=window.pageYOffset||document.documentElement.scrollTop;const scrollX=window.pageXOffset||document.documentElement.scrollLeft;const spaceAbove=linkRect.top;let top;if(spaceAbove>=previewRect.height+margin){top=linkRect.top+scrollY-previewRect.height-margin;preview.classList.add('link-preview--above');preview.classList.remove('link-preview--below');}else{top=linkRect.bottom+scrollY+margin;preview.classList.add('link-preview--below');preview.classList.remove('link-preview--above');}
let left=linkRect.left+scrollX+(linkRect.width/2)-(CONFIG.previewWidth/2);left=Math.max(margin,Math.min(left,window.innerWidth+scrollX-CONFIG.previewWidth-margin));preview.style.top=`${top}px`;preview.style.left=`${left}px`;}
function destroyPreview(){if(activeLink){activeLink.removeAttribute('aria-describedby');}
if(activePreview){activePreview.remove();activePreview=null;}
activeLink=null;}
function scheduleShow(link){if(link===activeLink){cancelHide();return;}
cancelShow();cancelHide();if(activePreview){destroyPreview();}
activeLink=link;hoverTimeout=setTimeout(async()=>{hoverTimeout=null;if(activeLink!==link)return;const data=await fetchPreviewData(link.pathname,link);if(data&&activeLink===link&&!activePreview){activePreview=createPreviewCard(data,link);}},CONFIG.hoverDelay);}
function scheduleHide(){cancelShow();hideTimeout=setTimeout(()=>{destroyPreview();},CONFIG.hideDelay);}
function cancelShow(){if(hoverTimeout){clearTimeout(hoverTimeout);hoverTimeout=null;}
if(prefetchTimeout){clearTimeout(prefetchTimeout);prefetchTimeout=null;}
if(!activePreview){activeLink=null;}}
function cancelHide(){if(hideTimeout){clearTimeout(hideTimeout);hideTimeout=null;}}
function handleMouseOver(event){if(!event.target||typeof event.target.closest!=='function')return;const link=event.target.closest('a');if(!link||!isPreviewable(link))return;if(link===activeLink){cancelHide();if(!activePreview&&!hoverTimeout){scheduleShow(link);}
return;}
prefetch(link);scheduleShow(link);}
function handleMouseOut(event){if(!event.target||typeof event.target.closest!=='function')return;const link=event.target.closest('a');if(!link)return;const relatedTarget=event.relatedTarget;if(relatedTarget&&typeof relatedTarget.closest==='function'){if(link.contains(relatedTarget))return;if(activePreview&&activePreview.contains(relatedTarget))return;}
scheduleHide();}
function handleFocusIn(event){const link=event.target.closest('a');if(!link||!isPreviewable(link))return;scheduleShow(link);}
function handleFocusOut(){scheduleHide();}
function handleKeyDown(event){if(event.key==='Escape'&&activePreview){destroyPreview();}}
function handleTouchStart(event){const link=event.target.closest('a');if(!link||!isPreviewable(link))return;touchStartTime=Date.now();touchStartPos={x:event.touches[0].clientX,y:event.touches[0].clientY};prefetch(link);touchTimeout=setTimeout(async()=>{event.preventDefault();const data=await fetchPreviewData(link.pathname,link);if(data&&!activePreview){activeLink=link;activePreview=createPreviewCard(data,link);if(navigator.vibrate)navigator.vibrate(10);}},CONFIG.longPressDelay);}
function handleTouchMove(event){if(!touchTimeout)return;const touch=event.touches[0];const deltaX=Math.abs(touch.clientX-touchStartPos.x);const deltaY=Math.abs(touch.clientY-touchStartPos.y);if(deltaX>10||deltaY>10){clearTimeout(touchTimeout);touchTimeout=null;}}
function handleTouchEnd(event){clearTimeout(touchTimeout);if(Date.now()-touchStartTime<CONFIG.longPressDelay){if(activePreview){event.preventDefault();destroyPreview();}
return;}
if(activePreview){event.preventDefault();}}
function handleDocumentClick(event){if(!activePreview)return;if(!activePreview.contains(event.target)&&activeLink!==event.target&&!activeLink?.contains(event.target)){destroyPreview();}}
let initialized=false;function init(){if(initialized)return;initialized=true;if(CONFIG.debug){console.log('[LinkPreviews] Initializing with config:',CONFIG);}
document.addEventListener('mouseover',handleMouseOver);document.addEventListener('mouseout',handleMouseOut);document.addEventListener('focusin',handleFocusIn,true);document.addEventListener('focusout',handleFocusOut,true);document.addEventListener('keydown',handleKeyDown);document.addEventListener('touchstart',handleTouchStart,{passive:false});document.addEventListener('touchmove',handleTouchMove,{passive:true});document.addEventListener('touchend',handleTouchEnd,{passive:false});document.addEventListener('click',handleDocumentClick);document.addEventListener('turbo:before-visit',destroyPreview);document.addEventListener('astro:before-preparation',destroyPreview);let resizeTimeout;window.addEventListener('resize',()=>{clearTimeout(resizeTimeout);resizeTimeout=setTimeout(()=>{if(activePreview&&activeLink){positionPreview(activeLink,activePreview);}},100);});}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);}else{init();}
window.BengalLinkPreviews={destroy:destroyPreview,clearCache:()=>cache.clear(),getConfig:()=>({...CONFIG}),isActive:()=>jsonAvailable,getDisabledHosts:()=>[...disabledHosts],getHostFailures:()=>Object.fromEntries(hostFailures),resetHost:(host)=>{disabledHosts.delete(host);hostFailures.delete(host);}};})();
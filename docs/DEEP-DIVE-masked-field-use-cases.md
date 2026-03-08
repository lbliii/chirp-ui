# Deep Dive: Masked Field Use Cases for ChirpUI

## Executive Summary

This document catalogs common masked input use cases that an average developer or end-user would expect from a form library. It informs which field primitives ChirpUI should add when integrating the [Alpine Mask plugin](https://alpinejs.dev/plugins/mask).

---

## Alpine Mask Capabilities (Reference)

### Wildcards

| Token | Description | Example |
|-------|-------------|---------|
| `9` | Numeric only (0-9) | `99/99/9999` → date |
| `a` | Alpha only (a-z, A-Z) | `aaa` → initials |
| `*` | Any character | `****` → promo code |

### APIs

- **`x-mask="pattern"`** — Static mask (e.g. `(999) 999-9999`)
- **`x-mask:dynamic="expression"`** — Dynamic mask based on `$input`
- **`$money($input, decimalSep, thousandsSep, precision)`** — Built-in currency helper

### Limitations

- No optional characters (e.g. ZIP+4 `99999-9999` vs `99999` — Alpine can't express "optional suffix")
- No strict character limit enforcement (excess chars may be typed but not displayed)
- No built-in SSN, phone, or date helpers — only `$money()`

---

## Use Case Brainstorm (By Domain)

### Tier 1: Universal (Every App Type)

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **Phone (US)** | `(999) 999-9999` | ✅ | Most common; 64% of e-commerce sites don't use it (Baymard) |
| **Email** | N/A | ❌ | Validation, not masking; use `type="email"` |
| **Date (MM/DD/YYYY)** | `99/99/9999` | ✅ | Alternative to native `type="date"` for text-style entry |
| **Date (ISO)** | `9999-99-99` | ✅ | YYYY-MM-DD |
| **Time** | `99:99` or `99:99:99` | ✅ | HH:MM or HH:MM:SS |
| **Currency / Money** | `$money($input)` | ✅ | Alpine built-in; configurable decimal/thousands |
| **Percentage** | `99.99` or `999` | ✅ | Often combined with suffix `%` |
| **Integer** | `999999` | ✅ | Whole numbers, no decimals |

### Tier 2: E-Commerce & Checkout

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **Credit card** | Dynamic (Amex vs Visa/MC) | ✅ `x-mask:dynamic` | Amex: `9999 999999 99999`; Others: `9999 9999 9999 9999` |
| **Expiry date** | `99/99` | ✅ | MM/YY |
| **CVV** | `999` or `9999` | ✅ | 3 or 4 digits |
| **ZIP (US 5-digit)** | `99999` | ✅ | Basic US postal |
| **ZIP+4** | `99999-9999` | ✅ | Full US; optional `-9999` not supported in Alpine |
| **Postal (Canada)** | `a9a 9a9` | ✅ | Canadian format |
| **Postal (UK)** | `aa9 9aa` or `aa99 9aa` | ✅ | UK postcodes vary |
| **Order/Invoice #** | `ORD-999999` | ✅ | Custom prefix + digits |
| **Promo/coupon code** | `****-****` | ✅ | Alphanumeric, variable length |

### Tier 3: Finance & Banking

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **Routing number (US)** | `999999999` | ✅ | 9 digits, no separators (or `999-999-999`) |
| **Account number** | `99999999999999` | ✅ | Variable length; mask length = max |
| **IBAN** | `aa99 9999 9999 9999 9999 99` | ✅ | Country-specific; simplified |
| **SWIFT/BIC** | `aaaaaabbccc` | ✅ | 8 or 11 chars, alphanumeric |
| **Tax ID (EIN)** | `99-9999999` | ✅ | US Employer ID |
| **Sort code (UK)** | `99-99-99` | ✅ | UK bank sort code |

### Tier 4: Government & Identity

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **SSN (US)** | `999-99-9999` | ✅ | Social Security Number |
| **Passport number** | `a9999999` | ✅ | Varies by country |
| **Driver's license** | `*********` | ✅ | Alphanumeric, state-specific |
| **National ID** | Varies | ⚠️ | Country-specific |

### Tier 5: Healthcare & Insurance

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **Member ID** | `999999999` | ✅ | Insurance member number |
| **Group number** | `99999` | ✅ | Insurance group |
| **NPI (US)** | `9999999999` | ✅ | 10-digit National Provider ID |
| **DEA number** | `aa9999999` | ✅ | Drug Enforcement Admin |
| **ICD code** | `a99.99` | ✅ | Diagnosis codes |

### Tier 6: Logistics & Inventory

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **Tracking number** | `***********` | ✅ | UPS, FedEx, USPS vary |
| **SKU** | `aaa-9999` | ✅ | Product codes |
| **VIN** | `99999999999999999` | ✅ | 17 chars; validation separate |
| **Barcode / UPC** | `99999999999` | ✅ | 12 digits typical |
| **Lot/batch number** | `*********` | ✅ | Alphanumeric |

### Tier 7: Developer & Technical

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **IP address** | `999.999.999.999` | ✅ | IPv4 |
| **Hex color** | `#aaaaaa` | ⚠️ | Alpine has `a` for alpha; hex needs `[0-9a-fA-F]` — Alpine `*` works |
| **Version number** | `99.99.99` | ✅ | Semver-style |
| **MAC address** | `aa:aa:aa:aa:aa:aa` | ✅ | Network hardware |
| **API key** | `****-****-****-****` | ✅ | Dash-separated |

### Tier 8: International & Localization

| Use Case | Mask Pattern | Alpine Compatible | Notes |
|----------|--------------|-------------------|-------|
| **Phone (UK)** | `9999 999 9999` | ✅ | UK mobile |
| **Phone (EU)** | `+99 999 999 9999` | ✅ | Country code + variable |
| **Phone (Brazil)** | `(99) 99999-9999` | ✅ | Mobile with 9th digit |
| **Date (EU)** | `99.99.9999` | ✅ | DD.MM.YYYY |
| **Date (ISO)** | `9999-99-99` | ✅ | YYYY-MM-DD |
| **Money (EU)** | `$money($input, ',', '.')` | ✅ | Comma decimal, period thousands |
| **Money (JP)** | `$money($input, '.', ',', 0)` | ✅ | No decimals, comma thousands |

---

## Prioritization for ChirpUI

### High Priority (Implement First)

1. **`phone_field`** — `(999) 999-9999` (US default), optional `format` param for locale
2. **`money_field`** — `$money($input)` with decimal/thousands/precision params
3. **`masked_field`** — Generic `mask` / `mask_dynamic` passthrough for custom patterns

### Medium Priority (Common Enough)

4. **`credit_card_field`** — Dynamic Amex vs Visa/MC (or document as `masked_field` example)
5. **`date_masked_field`** — `99/99/9999` for text-style date (distinct from native `date_field`)
6. **`ssn_field`** — `999-99-9999`
7. **`expiry_field`** — `99/99` for card expiry

### Lower Priority (Niche or Easy to DIY)

8. **`zip_field`** — `99999` or `99999-9999`; many apps use plain text + validation
9. **`routing_field`** — `999999999`; finance-specific
10. **`time_field`** — `99:99`; native `type="time"` often sufficient

### Document-Only (No New Macro)

- **IP, MAC, hex color, VIN, tracking** — Use `masked_field` with custom mask; document examples in showcase

---

## Form Library Comparison

| Library | Presets | Notes |
|---------|---------|-------|
| **SurveyJS** | numeric, currency, datetime, pattern | 4 mask types; pattern uses `9`, `a`, `#` |
| **FormKit** | Custom tokens `#`, `a`, `*`, `h` (hex) | Pro feature; rich token system |
| **jQuery Mask Plugin** | Pattern-based | `9`, `a`, `*`, `?` (optional) |
| **USWDS** | SSN, phone, date, zip | US government design system |
| **Alpine Mask** | `9`, `a`, `*`, `$money()` | Minimal; dynamic for complex cases |

---

## Implementation Notes for ChirpUI

1. **`masked_field`** should accept:
   - `mask` — static pattern → `x-mask`
   - `mask_dynamic` — expression → `x-mask:dynamic`
   - All other `text_field` params (label, errors, hint, attrs, etc.)

2. **`phone_field`** could support:
   - `format="us"` (default) → `(999) 999-9999`
   - `format="us-ext"` → `(999) 999-9999 x999`
   - `format="uk"` → `9999 999 9999`
   - `format="intl"` → `+9 999 999 9999` (simplified)
   - Or just `mask` param to override

3. **`money_field`** wraps `$money($input, decimal, thousands, precision)` with optional `prefix` (e.g. `$`, `€`).

4. **Alpine Mask plugin** must be loaded before Alpine core; document in app_shell_layout and README.

---

## References

- [Alpine Mask Plugin](https://alpinejs.dev/plugins/mask)
- [SurveyJS Masked Input](https://surveyjs.io/form-library/examples/masked-input-fields/documentation)
- [FormKit Mask Input](https://formkit.com/inputs/mask)
- [Baymard: Input Masking](https://baymard.com/blog/input-masking-form-field) — 64% of sites don't use it; reduces errors
- [E.164 Phone Format](https://en.wikipedia.org/wiki/E.164)
- [Gravity Forms Input Mask](https://docs.gravityforms.com/input-mask/)

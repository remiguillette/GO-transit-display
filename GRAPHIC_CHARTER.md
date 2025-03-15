
# GO Transit Display Board - Graphic Charter

## Brand Colors

Primary Colors:
- Black: #000000 (Background, Headers)
- White: #FFFFFF (Text, Content)
- Red: #FF0000 (Delays, Cancellations)
- Blue: #0052A5 (Accessibility Indicators)

Status Colors:
- Delayed: #FF0000
- On Time: #FFFFFF
- Platform: #FFFFFF

## Typography

Font Family: Polaris (Custom Font)
Variations:
- Polaris Bold: Headers, Important Information
- Polaris Medium: Navigation, Subheaders
- Polaris Light: Body Text, General Content

Font Sizes:
- Station Name: 42px
- Time Display: 48px
- Schedule Headers: 36px
- Schedule Rows: 36px

## Layout Elements

### Header Section
- Position: Top of viewport
- Height: Auto with padding 1.5rem
- Background: Black (#000000)
- Border Bottom: 2px solid var(--go-green)

### Logo Section
- Position: Left side of header
- Height: 40px
- Margin Right: 20px

### Station Info
- Position: Center of header
- Icon Size: 36px
- Name Size: 42px
- Letter Spacing: -0.02em

### Time Display
- Position: Right side of header
- Size: 48px
- Color: #FFFFFF
- Letter Spacing: -0.02em

### Schedule Grid
- Columns: 1fr 1.5fr 1.5fr 1fr
- Row Padding: 1rem 0.8rem
- Border Bottom: 1px solid #333
- Font: Polaris Light, 36px

## Responsive Breakpoints

Large Screens (>1200px):
- Default sizes apply

Medium Screens (<=1200px):
- Station Name: 36px
- Time Display: 36px
- Schedule Text: 28px

Small Screens (<=768px):
- Station Name: 28px
- Time Display: 28px
- Schedule Text: 24px
- Grid: 1fr 1fr 1fr 0.5fr

## Accessibility

- Minimum Contrast Ratio: 4.5:1
- Focus Indicators: 2px solid outline
- Alert Messages: Background #FF0000, White text
- Screen Reader Compatible HTML Structure

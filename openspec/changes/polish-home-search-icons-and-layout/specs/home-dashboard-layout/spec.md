## ADDED Requirements

### Requirement: Home keeps blog left and quick write right
The home page SHALL use stable left and right regions where blogs remain on the left and quick writes remain on the right.

#### Scenario: Desktop home layout
- **WHEN** the user views the home page on a desktop-width screen
- **THEN** the blog region MUST appear on the left and the quick write region MUST appear on the right

#### Scenario: Quick write composer belongs to right region
- **WHEN** the current user can publish quick writes
- **THEN** the quick write composer MUST appear in the right quick write region instead of above the blog region

#### Scenario: Page uses available width
- **WHEN** the user views the home page on a normal desktop viewport
- **THEN** the main content MUST reduce excessive side whitespace and give useful width to the blog and quick write regions

### Requirement: Home right region contains calendar above quick writes
The home page SHALL place the month calendar above quick write content in the right region.

#### Scenario: Calendar appears above quick writes
- **WHEN** the home page has enough width to show the month calendar
- **THEN** the calendar MUST appear above the quick write composer and quick write list in the right region

#### Scenario: Calendar collapses on very narrow width
- **WHEN** the right region is too narrow to render the month grid clearly
- **THEN** the calendar MUST collapse to a compact entry showing calendar text instead of forcing the month grid to render

### Requirement: Home compression preserves relative positions
The home page SHALL compress margins, widths, and calendar detail on narrow screens without changing the relative positions of the todo guide, blog region, and quick write region.

#### Scenario: Blog remains left on narrow width
- **WHEN** the home page is viewed on a narrow screen
- **THEN** the blog region MUST remain on the left side of the content layout

#### Scenario: Quick write remains right on narrow width
- **WHEN** the home page is viewed on a narrow screen
- **THEN** the quick write region MUST remain on the right side of the content layout

#### Scenario: Todo guide remains far left
- **WHEN** the home page is viewed on any supported width
- **THEN** the todo guide MUST remain at the far left as a compact guide or drawer and MUST NOT become a large content block that covers the main regions

#### Scenario: Horizontal overflow is allowed to preserve layout
- **WHEN** the viewport is too narrow to keep all regions readable through compression alone
- **THEN** the page MAY use horizontal overflow while still preserving the left todo, left blog, and right quick write relationship


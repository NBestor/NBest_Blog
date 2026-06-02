## ADDED Requirements

### Requirement: Quick post search result opens detail page
The system SHALL allow quick write search results to open the corresponding quick write detail page.

#### Scenario: Activate quick write result
- **WHEN** the user clicks or taps a quick write item in search results
- **THEN** the system MUST navigate to the selected quick write detail page

#### Scenario: Detail respects visibility
- **WHEN** the user opens a quick write detail page from search results
- **THEN** the detail page MUST still enforce the quick write visibility rules for the current user


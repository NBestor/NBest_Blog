## ADDED Requirements

### Requirement: Search blogs and quick posts
The system SHALL search blog content and quick write content, and MUST NOT search quick notes, todos, or calendar items from the global search entry.

#### Scenario: Search returns blog and quick write groups
- **WHEN** the user submits a global search query
- **THEN** the system MUST return blog results and quick write results as separate groups

#### Scenario: Quick write content is searchable
- **WHEN** a visible quick write contains the submitted query text
- **THEN** the quick write MUST appear in the quick write search result group

#### Scenario: Quick notes are excluded
- **WHEN** a private quick note contains the submitted query text
- **THEN** the quick note MUST NOT appear in global search results

### Requirement: Search preserves quick write visibility
The system SHALL apply existing quick write visibility rules when searching quick write content.

#### Scenario: Invisible quick write is excluded
- **WHEN** a quick write matches the submitted query but is not visible to the current user
- **THEN** the quick write MUST NOT appear in search results

#### Scenario: Visible quick write is included
- **WHEN** a quick write matches the submitted query and is visible to the current user
- **THEN** the quick write MUST be eligible for the quick write search result group

### Requirement: Search results keep left and right layout
The search results page SHALL display blog results on the left and quick write results on the right.

#### Scenario: Desktop search layout
- **WHEN** the user views search results on a desktop-width screen
- **THEN** blog results MUST appear in the left column and quick write results MUST appear in the right column

#### Scenario: Narrow search layout
- **WHEN** the user views search results on a narrow screen
- **THEN** the page MUST preserve the left blog and right quick write relationship instead of stacking the two groups vertically

#### Scenario: Quick write result opens detail
- **WHEN** the user activates a quick write search result
- **THEN** the system MUST navigate to that quick write detail view


Feature: Compare Extracts
  Scenario: Column name match in both the extracts
    Given last week csv file input
    And latest csv file input
    When column names of the files are compared
    Then  no unmatched column names should be found
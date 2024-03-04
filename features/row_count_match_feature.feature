Feature: Compare Extracts
  Scenario: Row count match in both the extracts
    Given last week csv file input
    And latest csv file input
    When row count of the files are compared
    Then  row count should be equal
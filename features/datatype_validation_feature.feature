Feature: Data Type Validation
  Scenario: Data Type should match with the config file
    Given extract file input
    And config csv file input
    When data type of the extract file is compared with config file
    Then  no unmatched data type should be found
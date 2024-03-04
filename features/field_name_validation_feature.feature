Feature: Field name validation
  Scenario: Field name should match with the config file
    Given extract file input
    And config csv file input
    When field names of the extract file is compared with config file
    Then  no unmatched field names should be found
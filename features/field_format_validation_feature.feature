Feature: Field Format Validation
  Scenario: Field format should match with the config file
    Given extract file input
    And config csv file input
    When field format of the extract file is compared with config file
    Then  no unmatched field formats should be found
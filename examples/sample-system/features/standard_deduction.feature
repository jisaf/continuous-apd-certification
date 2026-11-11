@rule:fna:sirt:S0215
Feature: Standard deduction by household size
  SIRT OD-1 (7 CFR 273.9(d)(1)): does the system correctly calculate the standard deduction based on
  household size? Values are the 18F prototype's FY2020 Illinois results (CC0).

  Scenario Outline: Benefit for a household with no income reflects the standard deduction
    Given an Illinois household of <size> people with no income
    When the system determines SNAP eligibility
    Then the household is eligible
    And the monthly benefit is $<benefit>

    Examples:
      | size | benefit |
      | 1    | 194     |
      | 2    | 355     |
      | 3    | 509     |

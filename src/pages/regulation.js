import React from 'react';
import { Link } from 'gatsby';
import Layout from '../components/layout';
import { Accordion, AccordionButton, AccordionContent } from '../lib';

const RegulationSection = ({ data }) => {
  return (
    <Layout>
      <div className="usa-layout-docs usa-section">
        <div className="grid-container">
          <div className="grid-row grid-gap">
            <aside className="usa-layout-docs-sidenav desktop:grid-col-3">
              <nav>
                <ul className="usa-sidenav">
                  <li className="usa-sidenav__item">
                    <Link to="regulation-tk" activeClassName="usa-current">
                      Subpart A - General §&nbsp;1041.1–§ 1041.3
                    </Link>
                  </li>
                  <li className="usa-sidenav__item">
                    <Link to="regulation-tk" activeClassName="usa-current">
                      Subpart B - Underwriting §&nbsp;1041.4–§ 1041.6
                    </Link>
                  </li>
                  <li className="usa-sidenav__item">
                    <Link to="regulation-tk" activeClassName="usa-current">
                      Subpart C - Payments §&nbsp;1041.7–§ 1041.9
                    </Link>
                  </li>
                  <li className="usa-sidenav__item">
                    <Link to="regulation" activeClassName="usa-current">
                      Subpart D - Information Furnishing, Recordkeeping, Anti-Evasion, Severability, and Dates §&nbsp;1041.10–§ 1041.15
                    </Link>
                    <ul className="usa-sidenav__sublist">
                      <li className="usa-sidenav__item">
                        <Link to="regulation" activeClassName="usa-current">
                          §&nbsp;1041.10 Information furnishing requirements.
                        </Link>
                      </li>
                      <li className="usa-sidenav__item">
                        <Link to="regulation-tk" activeClassName="usa-current">
                          §&nbsp;1041.11 Registered information systems.
                        </Link>
                      </li>
                      <li className="usa-sidenav__item">
                        <Link to="regulation-tk" activeClassName="usa-current">
                          §&nbsp;1041.12 Compliance program and record retention.
                        </Link>
                      </li>
                      <li className="usa-sidenav__item">
                        <Link to="regulation-tk" activeClassName="usa-current">
                          §&nbsp;1041.13 Prohibition against evasion.
                        </Link>
                      </li>
                      <li className="usa-sidenav__item">
                        <Link to="regulation-tk" activeClassName="usa-current">
                          §&nbsp;1041.14 Severability.
                        </Link>
                      </li>
                      <li className="usa-sidenav__item">
                        <Link to="regulation-tk" activeClassName="usa-current">
                          §&nbsp;1041.15 Effective and compliance dates.
                        </Link>
                      </li>
                    </ul>
                  </li>
                  <li className="usa-sidenav__item">
                    <Link to="regulation-tk" activeClassName="usa-current">
                      Appendices
                    </Link>
                  </li>
                  <li className="usa-sidenav__item">
                    <Link to="regulation-tk" activeClassName="usa-current">
                      Supplement I to Part 1041 - Official Interpretations
                    </Link>
                  </li>
                </ul>
              </nav>
            </aside>

            <div className="usa-layout-docs-main_content desktop:grid-col-9 usa-prose">
              <h1>§ 1041.10 Information furnishing requirements.</h1>
              <p>
                <b>(a) Loans subject to furnishing requirement.</b> For each covered short-term loan and covered longer-term balloon-payment loan a lender makes, the lender must furnish the loan information described in paragraph (c) of this section to each information system described in paragraph (b)(1) of this section.
              </p>
              <Accordion className="usa-accordion--bordered">
                <h2 className="usa-accordion__heading">
                  <AccordionButton controls="10-a-Interp">
                    Official interpretation of 10(a) Loans Subject to Furnishing Requirement
                  </AccordionButton>
                </h2>
                <AccordionContent id="10-a-Interp">
                  <p>
                    <b>1. Application to rollovers.</b> The furnishing requirements in § 1041.10(a) apply to each covered short-term loan or covered longer-term balloon-payment loan a lender makes, as well as to loans that are a rollover of a prior covered short-term loan or covered longer-term balloon-payment loan (or what is termed a “renewal” in some States). Rollovers are defined as a matter of State law but typically involve deferral of repayment of the principal amount of a short-term loan for a period of time in exchange for a fee. In the event that a lender is permitted under State law to roll over a covered short-term loan or covered longer-term balloon-payment loan and does so in accordance with the requirements of § 1041.5 or § 1041.6, the rollover would be treated, as applicable, as a new covered short-term loan or as a new covered longer-term balloon-payment loan for purposes of § 1041.10. For example, assume that a lender is permitted under applicable State law to roll over a covered short-term loan; the lender makes a covered short-term loan with a 14-day contractual duration; and on day 14 the lender reasonably determines that the consumer has the ability to repay a new loan under § 1041.5 and offers the consumer the opportunity to roll over the first loan for an additional 14 days. If the consumer accepts the rollover, the lender would report the original loan as no longer outstanding and would report the rollover as a new covered short-term loan.
                  </p>
                  <p>
                    <b>2. Furnishing through third parties.</b> Section 1041.10(a) requires that, for each covered short-term loan and covered longer-term balloon loan a lender makes, the lender must furnish the information concerning the loan described in § 1041.10(c) to each information system described in § 1041.10(b). A lender may furnish information to such information system directly, or may furnish through a third party acting on its behalf, including a provisionally registered or registered information system.
                  </p>
                </AccordionContent>
              </Accordion>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default RegulationSection;
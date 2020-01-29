import React from 'react';
import { Link } from 'gatsby';

const RegNav = () => {
    return (
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
    )
}

export default RegNav;
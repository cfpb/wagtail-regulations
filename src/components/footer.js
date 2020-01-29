import React from 'react';
import { Link } from 'gatsby';
import '../styles/footer.css'

const Footer = () => {
    return (
        <footer className="usa-footer usa-footer--slim">
  <div className="grid-container usa-footer__return-to-top">
    <Link to="#">Return to top</Link>
  </div>
  <div className="usa-footer__primary-section">
    <div className="usa-footer__primary-container grid-row">
      <div className="mobile-lg:grid-col-8">
        <nav className="usa-footer__nav">
          <ul className="grid-row grid-gap footer-list">
            <li className="mobile-lg:grid-col-6 desktop:grid-col-auto usa-footer__primary-content">
              <Link className="usa-footer__primary-link" to="javascript:void(0);">Primary link</Link>
            </li>
            <li className="mobile-lg:grid-col-6 desktop:grid-col-auto usa-footer__primary-content">
              <Link className="usa-footer__primary-link" to="javascript:void(0);">Primary link</Link>
            </li>
            <li className="mobile-lg:grid-col-6 desktop:grid-col-auto usa-footer__primary-content">
              <Link className="usa-footer__primary-link" to="javascript:void(0);">Primary link</Link>
            </li>
            <li className="mobile-lg:grid-col-6 desktop:grid-col-auto usa-footer__primary-content">
              <Link className="usa-footer__primary-link" to="javascript:void(0);">Primary link</Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="mobile-lg:grid-col-4">
        <address className="usa-footer__address">
          <div className="grid-row grid-gap">
            <div className="grid-col-auto mobile-lg:grid-col-12 desktop:grid-col-auto">
              <div className="usa-footer__contact-info">
                <Link to="tel:1-800-555-5555">(800) CALL-GOVT</Link>
              </div>
            </div>
            <div className="grid-col-auto mobile-lg:grid-col-12 desktop:grid-col-auto">
              <div className="usa-footer__contact-info">
                <Link to="mailto:info@agency.gov">info@agency.gov</Link>
              </div>
            </div>
          </div>
        </address>
      </div>
    </div>
  </div>
  <div className="usa-footer__secondary-section">
    <div className="grid-container">
      <div className="usa-footer__logo grid-row grid-gap-2">
        <div className="grid-col-auto">
          <h3 className="usa-footer__logo-heading">Name of Agency</h3>
        </div>
      </div>
    </div>
  </div>
  </footer>
    )
}

export default Footer;
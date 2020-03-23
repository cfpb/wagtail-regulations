import React from 'react';
import { Link } from 'gatsby';

const RegPagination = () => {
    return (
      <div className="grid-container reg-pagination">
        <div className="grid-row grid-gap">
          <div className="tablet:grid-col reg-pagination-column">
            <div className="reg-pagination-link">
              <Link to="regulation-tk">
                Previous section - § 1041.9
              </Link>
            </div>
            <div className="reg-pagination-title">
              § 1041.9 Disclosure of payment transfer attempts.
            </div>
          </div>
          <div className="tablet:grid-col reg-pagination-column">
            <div className="reg-pagination-link">
              <Link to="regulation-tk">
                Next section - § 1041.11
              </Link>
            </div>
            <div className="reg-pagination-title">
              § 1041.11 Registered information systems.
            </div>
          </div>
        </div>
      </div>
    )
}

export default RegPagination;
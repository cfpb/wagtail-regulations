import React from 'react';
import { Link } from 'gatsby';

const RegList = () => {
    return (
        <ul>
          <li>12 CFR Part 1002 - Equal Credit Opportunity Act (Regulation B)</li>
          <li>12 CFR Part 1003 - Home Mortgage Disclosure (Regulation C)</li>
          <li>12 CFR Part 1004 - Alternative Mortgage Transaction Parity (Regulation D)</li>
          <li>
            <Link to="regulation">
              12 CFR Part 1041 - Payday, Vehicle Title, and Certain High-Cost Installment Loans (Payday Lending Rule)
            </Link>
          </li>
        </ul>
    )
}

export default RegList;
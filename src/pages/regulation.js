import React from 'react';
import { Link } from 'gatsby';
import Layout from '../components/layout';
import RegNav from '../components/regnav';
import RegText from '../components/regtext';
import RegPagination from '../components/regpagination';
import { Accordion, AccordionButton, AccordionContent } from '../lib';

const RegulationSection = ({ data }) => {
  return (
    <Layout>
      <div className="usa-layout-docs usa-section">
        <div className="grid-container">
          <div className="grid-row grid-gap">
            
            <RegNav />

            <div className="usa-layout-docs-main_content desktop:grid-col-9 usa-prose">
              <h1>§ 1041.10 Information furnishing requirements.</h1>
              <RegText />
              <RegPagination />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default RegulationSection;
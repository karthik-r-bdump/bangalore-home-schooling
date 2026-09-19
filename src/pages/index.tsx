import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle" style={{maxWidth: '850px', margin: '0 auto 2rem auto'}}>
          {siteConfig.tagline}
        </p>
        <div className={styles.buttons} style={{display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap'}}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Explore All Subjects & Grades 📚
          </Link>
          <Link
            className="button button--outline button--secondary button--lg"
            to="/docs/homeschooling-guide/getting-started">
            Homeschooling in Bangalore Guide 🧭
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} | ICSE Curriculum Notes & Resources`}
      description="Open-source ICSE homeschooling portal for Bangalore and India. Notes, question banks, solved papers, and assets for Pre-KG to Class 10.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

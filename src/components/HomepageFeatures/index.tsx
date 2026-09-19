import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type StageItem = {
  title: string;
  badge: string;
  icon: string;
  description: string;
  link: string;
  subjects: string[];
};

const Stages: StageItem[] = [
  {
    title: 'Foundation Stage',
    badge: 'Pre-KG • LKG • UKG',
    icon: '🌱',
    description:
      'Play-based learning, phonemic awareness, sensory exploration, pre-math concepts, and motor skill development.',
    link: '/docs/foundation/overview',
    subjects: ['Phonics', 'Early Math', 'General Awareness', 'Art & Motor Skills'],
  },
  {
    title: 'Primary Stage',
    badge: 'Classes 1 to 5',
    icon: '🎒',
    description:
      'Foundational literacy, numeracy, environmental studies, basic social studies, and logical computer basics.',
    link: '/docs/primary/overview',
    subjects: ['English', 'Mathematics', 'EVS / Science', 'Social Studies', 'Hindi'],
  },
  {
    title: 'Middle School Stage',
    badge: 'Classes 6 to 8',
    icon: '🔬',
    description:
      'Transition to distinct science disciplines (Physics, Chemistry, Biology), History & Civics, Geography, and Algebra.',
    link: '/docs/middle-school/overview',
    subjects: ['Physics', 'Chemistry', 'Biology', 'History & Civics', 'Geography', 'Maths'],
  },
  {
    title: 'Secondary Stage (ICSE)',
    badge: 'Classes 9 & 10 (Board Exam)',
    icon: '🎓',
    description:
      'Rigorous ICSE Board preparation with chapter notes, specimen paper analysis, 10-year question banks, and Java BlueJ.',
    link: '/docs/secondary/overview',
    subjects: ['Julius Caesar', 'ICSE Science', 'Maths & GST', 'Toposheets', 'Java OOP'],
  },
];

type FeatureItem = {
  title: string;
  icon: string;
  description: string;
};

const Features: FeatureItem[] = [
  {
    title: '100% ICSE & CISCE Aligned',
    icon: '📘',
    description:
      'Meticulously structured to cover the Council for the Indian School Certificate Examinations (CISCE) curriculum across all standards.',
  },
  {
    title: 'Structured Question Banks',
    icon: '📝',
    description:
      'Includes MCQs, 2-mark definitions, 3-mark conceptual questions, and 5-mark structured questions complete with step-by-step marking schemes.',
  },
  {
    title: 'Bangalore Community Focus',
    icon: '🏡',
    description:
      'Guidance for homeschooling families in Bangalore and Karnataka—including RTE legal facts, local science museums, nature trails, and exam centers.',
  },
  {
    title: 'Free & Open Source Assets',
    icon: '🖨️',
    description:
      'Downloadable printable worksheets, formula sheets, high-yield diagrams, and interactive simulations for home study.',
  },
];

export default function HomepageFeatures(): ReactNode {
  return (
    <div className="container padding-vert--xl">
      <div className="text--center margin-bottom--xl">
        <Heading as="h2">Browse by Learning Stage</Heading>
        <p className="hero__subtitle">
          Comprehensive curriculum notes, worksheets, and resources organized from Pre-KG to Class 10
        </p>
      </div>

      <div className="row margin-bottom--xl">
        {Stages.map((stage, idx) => (
          <div key={idx} className="col col--3 margin-bottom--md">
            <Link to={stage.link} className="stage-card">
              <div className="stage-icon">{stage.icon}</div>
              <span className="badge-tag">{stage.badge}</span>
              <Heading as="h3">{stage.title}</Heading>
              <p style={{flexGrow: 1, fontSize: '0.95rem'}}>{stage.description}</p>
              <div style={{marginTop: '0.5rem'}}>
                <small style={{fontWeight: 600, color: 'var(--ifm-color-primary)'}}>
                  {stage.subjects.join(' • ')}
                </small>
              </div>
            </Link>
          </div>
        ))}
      </div>

      <hr className="margin-vert--xl" />

      <div className="text--center margin-bottom--xl">
        <Heading as="h2">Why Bangalore Home Schooling?</Heading>
        <p className="hero__subtitle">Built by parents and educators to make home education seamless</p>
      </div>

      <div className="row">
        {Features.map((feat, idx) => (
          <div key={idx} className="col col--6 margin-bottom--lg">
            <div className="card padding--lg" style={{height: '100%'}}>
              <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>{feat.icon}</div>
              <Heading as="h3">{feat.title}</Heading>
              <p>{feat.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

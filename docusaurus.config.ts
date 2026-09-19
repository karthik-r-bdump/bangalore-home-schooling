import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Bangalore Home Schooling',
  tagline: 'Comprehensive ICSE Curriculum Notes, Question Banks, and Learning Resources from Pre-KG to Class 10',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true,
  },

  // Set the production url of your site here
  url: 'https://karthik-r-bdump.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/bangalore-home-schooling/',

  // GitHub pages deployment config.
  organizationName: 'karthik-r-bdump',
  projectName: 'bangalore-home-schooling',
  trailingSlash: false,
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/karthik-r-bdump/bangalore-home-schooling/tree/main/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/karthik-r-bdump/bangalore-home-schooling/tree/main/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Bangalore Home Schooling (ICSE)',
      logo: {
        alt: 'Bangalore Home Schooling Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'curriculumSidebar',
          position: 'left',
          label: 'Curriculum & Notes',
        },
        {
          to: '/docs/homeschooling-guide/getting-started',
          label: 'Homeschooling Guide',
          position: 'left',
        },
        {to: '/blog', label: 'Community Updates', position: 'left'},
        {
          href: 'https://github.com/karthik-r-bdump/bangalore-home-schooling',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Stages',
          items: [
            {
              label: 'Foundation (Pre-KG to UKG)',
              to: '/docs/foundation/overview',
            },
            {
              label: 'Primary (Classes 1 - 5)',
              to: '/docs/primary/overview',
            },
            {
              label: 'Middle School (Classes 6 - 8)',
              to: '/docs/middle-school/overview',
            },
            {
              label: 'Secondary (Classes 9 - 10)',
              to: '/docs/secondary/overview',
            },
          ],
        },
        {
          title: 'Homeschooling Resources',
          items: [
            {
              label: 'Getting Started in Bangalore',
              to: '/docs/homeschooling-guide/getting-started',
            },
            {
              label: 'Curriculum Planning & Timetable',
              to: '/docs/homeschooling-guide/curriculum-planning',
            },
            {
              label: 'Assessment Rubrics & Tests',
              to: '/docs/homeschooling-guide/assessment-rubrics',
            },
            {
              label: 'Recommended Textbooks',
              to: '/docs/homeschooling-guide/recommended-books',
            },
            {
              label: 'Digital Assets & Printables',
              to: '/docs/homeschooling-guide/digital-assets-library',
            },
          ],
        },
        {
          title: 'Board & Community',
          items: [
            {
              label: 'CISCE Official Website',
              href: 'https://cisce.org',
            },
            {
              label: 'Bangalore Homeschoolers Forum',
              to: '/blog',
            },
            {
              label: 'Contribute on GitHub',
              href: 'https://github.com/karthik-r-bdump/bangalore-home-schooling',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Bangalore Home Schooling Community. Built with Docusaurus. Released under MIT License.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['java', 'bash', 'json', 'python'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

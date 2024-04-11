/**
 * @license Copyright 2017 Google Inc. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
 */
'use strict';
module.exports = {
  // 1. Run your custom tests along with all the default Lighthouse tests.
  // extends: 'lighthouse:default',
  onlyCategories: ['performance'],

  output: 'html',

  // 2. Add gatherer to the default Lighthouse load ('pass') of the page.
  passes: [{
    passName: 'defaultPass',
    gatherers: [
      'universalheader-gatherer',
    ],
  }],

  // 3. Add custom audit to the list of audits 'lighthouse:default' will run.
  audits: [
	'universalheader-audit',
  ],

  groups: {
    nodes: {
      title: 'Nodes group'
    },
    nesting: {
      title: 'Nesting group'
    },
    startup: {
      title: 'Startup group'
    },
  },

  // 4. Create a new section in the default report for our results.
  categories: {

    CorporateWiki: {
      title: 'Corporate Wiki',
      description: 'Corporate Wiki',
      auditRefs: [
		{ id: 'universalheader-audit', weight: 1 }
      ],
    },
  },
};

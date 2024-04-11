'use strict';

const Audit = require('lighthouse').Audit;

const MAX_DATA = 2000;

class UniversalHeaderAudit extends Audit {
    static get meta() {
        return {
            id: 'universalheader-audit',
            title: 'universalheader-audit',
            failureTitle: 'Universal Header is not on the page',
            description: 'Used to check if universal header is displayed on the page',

            // The name of the custom gatherer class that provides input to this audit.
            requiredArtifacts: ['UniversalHeaderGatherer'],
        };
    }

    static audit(artifacts) {
        const enwikiMetrics = artifacts.UniversalHeaderGatherer;
        // This score will be binary, so will get a red ✘ or green ✓ in the report.
        const belowThreshold = enwikiMetrics <= MAX_DATA;

        return {
            // true
            rawValue: enwikiMetrics,
            // Cast true/false to 1/0
            score: Number(belowThreshold),
        };
    }
}
module.exports = UniversalHeaderAudit;

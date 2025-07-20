// CyferTrace Security Scanner JavaScript

class SecurityScanner {
    constructor(scanType) {
        this.scanType = scanType;
        this.currentScanId = null;
        this.progressInterval = null;
        this.isScanning = false;
    }

    async startScan(endpoint, formData) {
        if (this.isScanning) {
            CyferTrace.showToast('A scan is already in progress', 'warning');
            return;
        }

        try {
            this.isScanning = true;
            this.showProgress();
            
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.error) {
                throw new Error(result.error);
            }

            this.currentScanId = result.scan_id;
            this.updateProgress(0, 'Scan started successfully...');
            
            if (result.status === 'completed') {
                // Scan completed immediately
                this.showResults(result.results);
            } else {
                // Start polling for progress
                this.startProgressPolling();
            }

        } catch (error) {
            console.error('Scan failed:', error);
            this.hideProgress();
            this.isScanning = false;
            CyferTrace.showToast(`Scan failed: ${error.message}`, 'error');
        }
    }

    showProgress() {
        const progressSection = document.getElementById('scanProgress');
        const formSection = progressSection.previousElementSibling;
        
        if (progressSection && formSection) {
            formSection.style.opacity = '0.5';
            progressSection.classList.remove('hidden');
            this.updateProgress(0, 'Initializing scan...');
            
            if (this.currentScanId) {
                document.getElementById('scanId').textContent = this.currentScanId;
            }
        }
    }

    hideProgress() {
        const progressSection = document.getElementById('scanProgress');
        const formSection = progressSection.previousElementSibling;
        
        if (progressSection && formSection) {
            progressSection.classList.add('hidden');
            formSection.style.opacity = '1';
        }
        
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        
        this.isScanning = false;
    }

    updateProgress(percentage, message) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const scanId = document.getElementById('scanId');
        
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }
        
        if (progressText) {
            progressText.textContent = message;
        }
        
        if (scanId && this.currentScanId) {
            scanId.textContent = this.currentScanId;
        }
    }

    startProgressPolling() {
        if (!this.currentScanId) return;
        
        let progress = 10;
        const progressMessages = this.getProgressMessages();
        let messageIndex = 0;
        
        this.progressInterval = setInterval(async () => {
            try {
                // Simulate progress increase
                progress = Math.min(progress + Math.random() * 15, 90);
                
                // Update message
                if (messageIndex < progressMessages.length) {
                    this.updateProgress(progress, progressMessages[messageIndex]);
                    messageIndex++;
                }
                
                // Check actual scan status
                const response = await fetch(`/api/scan/${this.currentScanId}/status`, {
                    credentials: 'include'
                });
                
                if (response.ok) {
                    const status = await response.json();
                    
                    if (status.status === 'completed') {
                        this.updateProgress(100, 'Scan completed successfully!');
                        setTimeout(() => {
                            this.showResults(status.results);
                        }, 1000);
                        return;
                    } else if (status.status === 'failed') {
                        throw new Error('Scan failed on server');
                    }
                }
            } catch (error) {
                console.error('Progress polling error:', error);
                this.hideProgress();
                CyferTrace.showToast('Scan monitoring failed', 'error');
            }
        }, 2000);
    }

    getProgressMessages() {
        if (this.scanType === 'was') {
            return [
                'Starting web application discovery...',
                'Crawling application structure...',
                'Analyzing authentication mechanisms...',
                'Testing for injection vulnerabilities...',
                'Checking for XSS vulnerabilities...',
                'Validating security headers...',
                'Scanning for OWASP Top 10 issues...',
                'Generating security report...',
                'Finalizing analysis...'
            ];
        } else {
            return [
                'Parsing infrastructure files...',
                'Analyzing cloud configurations...',
                'Checking security policies...',
                'Validating access controls...',
                'Scanning for misconfigurations...',
                'Checking compliance requirements...',
                'Analyzing resource permissions...',
                'Generating remediation suggestions...',
                'Finalizing report...'
            ];
        }
    }

    showResults(results) {
        this.hideProgress();
        
        const resultsSection = document.getElementById('scanResults');
        
        if (!resultsSection) {
            CyferTrace.showToast('Results section not found', 'error');
            return;
        }
        
        resultsSection.classList.remove('hidden');
        
        // Show summary
        this.displaySummary(results);
        
        // Show detailed findings
        if (this.scanType === 'was') {
            this.displayVulnerabilities(results.vulnerabilities || []);
        } else {
            this.displayIssues(results.issues || []);
        }
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        CyferTrace.showToast('Scan completed successfully!', 'success');
    }

    displaySummary(results) {
        const summaryContainer = document.getElementById('resultsSummary');
        const summary = results.summary || {};
        
        if (!summaryContainer) return;
        
        const totalItems = this.scanType === 'was' ? 'vulnerabilities' : 'issues';
        const total = summary[`total_${totalItems}`] || summary.total_vulnerabilities || summary.total_issues || 0;
        
        summaryContainer.innerHTML = `
            <div class="bg-white rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-gray-900 mb-2">${total}</div>
                <div class="text-gray-600">Total ${totalItems.charAt(0).toUpperCase() + totalItems.slice(1)}</div>
            </div>
            <div class="bg-red-50 rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-red-600 mb-2">${summary.critical || 0}</div>
                <div class="text-red-800">Critical</div>
            </div>
            <div class="bg-orange-50 rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-orange-600 mb-2">${summary.high || 0}</div>
                <div class="text-orange-800">High</div>
            </div>
            <div class="bg-yellow-50 rounded-lg shadow p-6 text-center">
                <div class="text-3xl font-bold text-yellow-600 mb-2">${summary.medium || 0}</div>
                <div class="text-yellow-800">Medium</div>
            </div>
        `;
    }

    displayVulnerabilities(vulnerabilities) {
        const container = document.getElementById('vulnerabilitiesList');
        
        if (!container) return;
        
        if (vulnerabilities.length === 0) {
            container.innerHTML = `
                <div class="text-center py-12">
                    <i class="fas fa-shield-alt text-green-500 text-6xl mb-4"></i>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">No Vulnerabilities Found</h3>
                    <p class="text-gray-600">Great! Your web application appears to be secure.</p>
                </div>
            `;
            return;
        }
        
        const groupedVulns = this.groupBySeverity(vulnerabilities, 'severity');
        let html = '<div class="space-y-6">';
        
        ['Critical', 'High', 'Medium', 'Low'].forEach(severity => {
            const vulns = groupedVulns[severity] || [];
            if (vulns.length === 0) return;
            
            html += `
                <div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <span class="severity-badge severity-${severity.toLowerCase()} px-3 py-1 rounded-full text-sm mr-3">${severity}</span>
                        ${vulns.length} ${vulns.length === 1 ? 'vulnerability' : 'vulnerabilities'}
                    </h4>
                    <div class="space-y-4">
            `;
            
            vulns.forEach((vuln, index) => {
                html += `
                    <div class="vulnerability-item ${severity.toLowerCase()} bg-white rounded-lg border shadow p-6">
                        <div class="flex items-start justify-between mb-4">
                            <h5 class="text-lg font-semibold text-gray-900">${this.escapeHtml(vuln.name)}</h5>
                            <div class="flex items-center space-x-2">
                                <span class="severity-badge severity-${severity.toLowerCase()} px-2 py-1 rounded text-xs">${severity}</span>
                                ${vuln.confidence ? `<span class="bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs">Confidence: ${vuln.confidence}</span>` : ''}
                            </div>
                        </div>
                        
                        ${vuln.description ? `<p class="text-gray-600 mb-4">${this.escapeHtml(vuln.description)}</p>` : ''}
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            ${vuln.location ? `
                                <div>
                                    <span class="text-sm font-medium text-gray-500">Location:</span>
                                    <p class="text-sm text-gray-900 font-mono break-all">${this.escapeHtml(vuln.location)}</p>
                                </div>
                            ` : ''}
                            ${vuln.cwe ? `
                                <div>
                                    <span class="text-sm font-medium text-gray-500">CWE ID:</span>
                                    <p class="text-sm text-gray-900">${this.escapeHtml(vuln.cwe)}</p>
                                </div>
                            ` : ''}
                        </div>
                        
                        ${vuln.solution ? `
                            <div class="bg-blue-50 rounded-lg p-4">
                                <h6 class="text-sm font-medium text-blue-800 mb-2">Recommended Fix:</h6>
                                <p class="text-sm text-blue-700">${this.escapeHtml(vuln.solution)}</p>
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            html += '</div></div>';
        });
        
        html += '</div>';
        container.innerHTML = html;
    }

    displayIssues(issues) {
        const container = document.getElementById('issuesList');
        
        if (!container) return;
        
        if (issues.length === 0) {
            container.innerHTML = `
                <div class="text-center py-12">
                    <i class="fas fa-check-circle text-green-500 text-6xl mb-4"></i>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">No Issues Found</h3>
                    <p class="text-gray-600">Your infrastructure configuration looks secure!</p>
                </div>
            `;
            return;
        }
        
        const groupedIssues = this.groupBySeverity(issues, 'severity');
        let html = '<div class="space-y-6">';
        
        ['Critical', 'High', 'Medium', 'Low'].forEach(severity => {
            const severityIssues = groupedIssues[severity] || [];
            if (severityIssues.length === 0) return;
            
            html += `
                <div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <span class="severity-badge severity-${severity.toLowerCase()} px-3 py-1 rounded-full text-sm mr-3">${severity}</span>
                        ${severityIssues.length} ${severityIssues.length === 1 ? 'issue' : 'issues'}
                    </h4>
                    <div class="space-y-4">
            `;
            
            severityIssues.forEach((issue, index) => {
                html += `
                    <div class="vulnerability-item ${severity.toLowerCase()} bg-white rounded-lg border shadow p-6">
                        <div class="flex items-start justify-between mb-4">
                            <h5 class="text-lg font-semibold text-gray-900">${this.escapeHtml(issue.check_name || issue.name || 'Configuration Issue')}</h5>
                            <div class="flex items-center space-x-2">
                                <span class="severity-badge severity-${severity.toLowerCase()} px-2 py-1 rounded text-xs">${severity}</span>
                                ${issue.check_id ? `<span class="bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs">${issue.check_id}</span>` : ''}
                            </div>
                        </div>
                        
                        ${issue.description ? `<p class="text-gray-600 mb-4">${this.escapeHtml(issue.description)}</p>` : ''}
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            ${issue.resource ? `
                                <div>
                                    <span class="text-sm font-medium text-gray-500">Resource:</span>
                                    <p class="text-sm text-gray-900 font-mono">${this.escapeHtml(issue.resource)}</p>
                                </div>
                            ` : ''}
                            ${issue.file_path ? `
                                <div>
                                    <span class="text-sm font-medium text-gray-500">File:</span>
                                    <p class="text-sm text-gray-900 font-mono break-all">${this.escapeHtml(issue.file_path)}</p>
                                </div>
                            ` : ''}
                            ${issue.line_range && issue.line_range.length > 0 ? `
                                <div>
                                    <span class="text-sm font-medium text-gray-500">Lines:</span>
                                    <p class="text-sm text-gray-900">${issue.line_range.join('-')}</p>
                                </div>
                            ` : ''}
                        </div>
                        
                        ${issue.remediation || issue.guideline ? `
                            <div class="bg-green-50 rounded-lg p-4">
                                <h6 class="text-sm font-medium text-green-800 mb-2">Remediation:</h6>
                                <p class="text-sm text-green-700">${this.escapeHtml(issue.remediation || issue.guideline)}</p>
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            html += '</div></div>';
        });
        
        html += '</div>';
        container.innerHTML = html;
    }

    groupBySeverity(items, severityField) {
        const groups = {
            'Critical': [],
            'High': [],
            'Medium': [],
            'Low': []
        };
        
        items.forEach(item => {
            const severity = item[severityField] || 'Medium';
            if (groups[severity]) {
                groups[severity].push(item);
            } else {
                groups['Medium'].push(item);
            }
        });
        
        return groups;
    }

    escapeHtml(text) {
        if (typeof text !== 'string') return text;
        
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    reset() {
        this.currentScanId = null;
        this.hideProgress();
        
        const resultsSection = document.getElementById('scanResults');
        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }
        
        // Reset form
        const form = document.querySelector('form');
        if (form) {
            form.reset();
        }
    }
}

// Export for global access
window.SecurityScanner = SecurityScanner;

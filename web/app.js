document.addEventListener('DOMContentLoaded', () => {
    renderLDTrendChart();
    renderCandidateTable();
    renderLDTable();
    renderInternalLDTable();
    renderLeaves2025();
    renderLeaves2026();
    renderLeavesDonuts();
    renderBehavioralGrid();
});

function renderLDTrendChart() {
    const ctx = document.getElementById('ld-line-chart');
    if (!ctx) return;

    let gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 220);
    gradient.addColorStop(0, 'rgba(16, 185, 129, 0.2)');
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Internal Learning',
                    data: [8, 12, 10, 6, 9, 5, 3.3], // Example ~53.3 hours
                    backgroundColor: '#10B981', // green
                    borderRadius: 4
                },
                {
                    label: 'External Learning',
                    data: [3, 5, 2, 4, 6, 5, 2], // Example ~27 hours
                    backgroundColor: '#3B82F6', // blue
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
                        color: '#64748B'
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 }, color: '#94A3B8' }
                },
                y: {
                    border: { dash: [4, 4] },
                    grid: { color: '#F1F5F9', drawBorder: false },
                    ticks: { font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 }, color: '#94A3B8' }
                }
            }
        }
    });
}
function renderInternalLDTable() {
    const internalLD = [
        { course: "POSH Training 2025", status: "Completed", statusStyle: "green" },
        { course: "Information Security InfoSec", status: "Completed", statusStyle: "green" },
        { course: "Code of Conduct Refresher", status: "Completed", statusStyle: "green" },
        { course: "Data Privacy & Protection", status: "Pending", statusStyle: "red" },
        { course: "Diversity & Inclusion Basics", status: "Completed", statusStyle: "green" }
    ];

    const tbody = document.getElementById('ld-internal-table');
    if (tbody) {
        tbody.innerHTML = internalLD.map(l => `
            <tr>
                <td>${l.course}</td>
                <td><span class="status-badge ${l.statusStyle}">${l.status}</span></td>
            </tr>
        `).join('');
    }
}


function renderCandidateTable() {
    // Top priority detailed list
    const candidates = [
        { name: "Alan Pinto", role: "VMO Project Support", skills: "Project Mgt, Support", client: "Lupin", loc: "Airoli", doj: "14-Jul-25", color: "10B981" },
        { name: "Shivappa Tekale", role: "SAP SD Invoicing Architect", skills: "SAP SD", client: "Hitachi", loc: "Bangalore", doj: "13-Aug-25", color: "3B82F6" },
        { name: "Manoj R.", role: "SAP CRM / C4C", skills: "SAP CRM, C4C", client: "Hitachi", loc: "Bangalore", doj: "14-Aug-25", color: "10B981" },
        { name: "Neelufar A", role: "HR Assistant", skills: "HR, Admin", client: "Amazon", loc: "Bangalore", doj: "22-Dec-25", color: "3B82F6" },
        { name: "Bukya Santhosh", role: "Infra (Azure) Engineer", skills: "Azure Cloud, Infra", client: "Hitachi", loc: "Hyderabad", doj: "05-Mar-26", color: "10B981" },
        { name: "Sahare Ratnabodhi", role: "E2E Quality Assurance", skills: "QA, E2E Testing", client: "Amazon", loc: "Bangalore", doj: "10-Mar-26", color: "3B82F6" }
    ];

    const tbody = document.getElementById('candidate-table');
    tbody.innerHTML = candidates.map(c => `
        <tr>
            <td>
                <div class="candidate-avatar-cell">
                    <img src="https://ui-avatars.com/api/?name=${encodeURIComponent(c.name)}&background=${c.color}&color=fff" alt="">
                    <span>${c.name}</span>
                </div>
            </td>
            <td>${c.role}</td>
            <td style="color:#64748B;">${c.skills}</td>
            <td>${c.client}</td>
            <td>${c.loc}</td>
            <td>${c.doj}</td>
            <td><span class="status-badge green">Joined</span></td>
        </tr>
    `).join('');
}

function renderLDTable() {
    const externalLD = [
        { course: "LinkedIn AI Recruiter", type: "LinkedIn", grade: "Dec-25", status: "Completed", statusStyle: "blue" },
        { course: "Talent Success Updates", type: "LinkedIn", grade: "Sep-25", status: "Completed", statusStyle: "blue" },
        { course: "Critical Skills Assessment", type: "LinkedIn", grade: "Oct-25", status: "Completed", statusStyle: "blue" },
        { course: "Master Python Prog.", type: "Self Learning", grade: "15 hrs", status: "90% In Prog", statusStyle: "orange" },
        { course: "MySQL Data Analysis", type: "Self Learning", grade: "12 hrs", status: "80% In Prog", statusStyle: "orange" }
    ];

    const tbody = document.getElementById('ld-external-table');
    tbody.innerHTML = externalLD.map(l => `
        <tr>
            <td>${l.course}</td>
            <td style="color:#64748B;">${l.type}</td>
            <td>${l.grade} &nbsp; <span class="status-badge ${l.statusStyle}">${l.status}</span></td>
        </tr>
    `).join('');
}

function getExhaustedStatus(type, provided, taken) {
    if (type === "Unlimited Vacation" || type === "Unlimited Vacation Leave") {
        return `<span class="status-badge green">Left (${provided - taken} Days)</span>`;
    }
    if (type === "Wellness Leave" || type === "Happiness Leave") {
        return `<span class="status-badge green">Completed</span>`;
    }
    if (taken > provided) {
        return `<span class="status-badge red">Exhausted (+${taken - provided} Extra)</span>`;
    }
    if (taken === provided) {
        return `<span class="status-badge red">Exhausted</span>`;
    }
    return `<span class="status-badge green">Left (${provided - taken})</span>`;
}

function renderLeaves2025() {
    const leaves25 = [
        { type: "Unlimited Vacation", prov: 15, taken: 6 },
        { type: "Casual Leave", prov: 3.5, taken: 4.5 },
        { type: "Sick Leave", prov: 3.5, taken: 4.5 },
        { type: "Wellness Leave", prov: 2, taken: 2 },
        { type: "Happiness Leave", prov: 1, taken: 1 }
    ];

    const tbody = document.getElementById('leaves-2025');
    tbody.innerHTML = leaves25.map(l => `
        <tr>
            <td>${l.type}</td>
            <td>${l.prov} Days</td>
            <td style="font-weight:700;">${l.taken} Days</td>
            <td>${getExhaustedStatus(l.type, l.prov, l.taken)}</td>
        </tr>
    `).join('');
}

function renderLeaves2026() {
    const leaves26 = [
        { type: "Unlimited Vacation", prov: 20, taken: 4 },
        { type: "Casual Leave", prov: 6, taken: 0 },
        { type: "Sick Leave", prov: 6, taken: 4 },
        { type: "Wellness Leave", prov: 2, taken: 0 },
        { type: "Happiness Leave", prov: 1, taken: 0 }
    ];

    const tbody = document.getElementById('leaves-2026');
    tbody.innerHTML = leaves26.map(l => `
        <tr>
            <td>${l.type}</td>
            <td>${l.prov} Days</td>
            <td style="font-weight:700;">${l.taken} Days</td>
            <td>${getExhaustedStatus(l.type, l.prov, l.taken)}</td>
        </tr>
    `).join('');
}

function renderLeavesDonuts() {
    const ctx25 = document.getElementById('leaves-donut-2025');
    if (ctx25) {
        new Chart(ctx25, {
            type: 'doughnut',
            data: {
                labels: ['Taken (18)', 'Remaining (7)'],
                datasets: [{
                    data: [18, 7],
                    backgroundColor: ['#3B82F6', '#E2E8F0'],
                    borderWidth: 0,
                    cutout: '65%'
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20, font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 } } } }
            }
        });
    }

    const ctx26 = document.getElementById('leaves-donut-2026');
    if (ctx26) {
        new Chart(ctx26, {
            type: 'doughnut',
            data: {
                labels: ['Taken (8)', 'Remaining (27)'],
                datasets: [{
                    data: [8, 27],
                    backgroundColor: ['#3B82F6', '#E2E8F0'],
                    borderWidth: 0,
                    cutout: '65%'
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20, font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 } } } }
            }
        });
    }
}

function renderBehavioralGrid() {
    const behaviors = [
        {
            title: "Team Collaboration",
            icon: "👥",
            items: [
                "Collaborated in sourcing and sharing suitable profiles.",
                "Supported interview coordination smoothly.",
                "Shared market insights and candidate updates."
            ]
        },
        {
            title: "Process Discipline",
            icon: "📋",
            items: [
                "Maintained accurate recruitment trackers.",
                "Ensured timely updates on submissions.",
                "Followed recruitment processes consistently."
            ]
        },
        {
            title: "Client Communication",
            icon: "💬",
            items: [
                "Provided regular updates on candidate pipeline.",
                "Coordinated with hiring managers for feedback.",
                "Maintained clear communication internally."
            ]
        },
        {
            title: "Ownership & Conduct",
            icon: "🌟",
            items: [
                "Managed requirements from sourcing to coordination.",
                "Maintained professional, respectful communication.",
                "Demonstrated a positive, solution-oriented approach."
            ]
        }
    ];

    const container = document.getElementById('behavioral-grid');
    container.innerHTML = behaviors.map(b => `
        <div class="b-card">
            <div class="b-card-header">
                <div class="b-card-icon"><span>${b.icon}</span></div>
                <h4>${b.title}</h4>
            </div>
            <ul>
                ${b.items.map(i => `<li>${i}</li>`).join('')}
            </ul>
        </div>
    `).join('');
}

/* ============================================
   🎮 SIMULATION ENGINE - JavaScript
   Supermarket Queue Simulation Dashboard
   ============================================ */

// Simulation State
const state = {
    running: false,
    paused: false,
    simTime: 0,
    customers: [],
    queue: [],
    counters: [
        { id: 1, busy: false, customer: null, endTime: 0, served: 0 },
        { id: 2, busy: false, customer: null, endTime: 0, served: 0 },
        { id: 3, busy: false, customer: null, endTime: 0, served: 0 }
    ],
    completed: 0,
    totalWaitTime: 0,
    nextCustomerId: 1,
    nextArrivalTime: 0,
    speed: 5
};

// Configuration
const config = {
    meanInterArrival: 1.0,  // minutes
    meanServiceTime: 2.5,   // minutes
    maxSimTime: 60,         // minutes to simulate
    tickInterval: 50        // ms per tick
};

// DOM Elements
const elements = {
    startBtn: document.getElementById('btn-start'),
    pauseBtn: document.getElementById('btn-pause'),
    resetBtn: document.getElementById('btn-reset'),
    speedSlider: document.getElementById('speed-slider'),
    queueDisplay: document.getElementById('queue-display'),
    queueLength: document.getElementById('queue-length'),
    completedCount: document.getElementById('completed-count'),
    simTime: document.getElementById('sim-time'),
    arrivedCount: document.getElementById('arrived-count'),
    liveAvgWait: document.getElementById('live-avg-wait'),
    counters: [
        document.getElementById('counter-1'),
        document.getElementById('counter-2'),
        document.getElementById('counter-3')
    ]
};

// Utility: Exponential random variable
function exponentialRandom(mean) {
    return -mean * Math.log(1 - Math.random());
}

// Schedule next arrival
function scheduleNextArrival() {
    const interArrival = exponentialRandom(config.meanInterArrival);
    state.nextArrivalTime = state.simTime + interArrival;
}

// Create a new customer
function createCustomer() {
    const serviceTime = Math.max(0.5, exponentialRandom(config.meanServiceTime));
    const customer = {
        id: state.nextCustomerId++,
        arrivalTime: state.simTime,
        serviceTime: serviceTime,
        startServiceTime: null,
        endServiceTime: null
    };
    state.customers.push(customer);
    state.queue.push(customer);
    updateQueueDisplay();
    updateMetrics();
    scheduleNextArrival();
}

// Find available counter
function findAvailableCounter() {
    return state.counters.find(c => !c.busy);
}

// Start serving customer
function startService(counter, customer) {
    customer.startServiceTime = state.simTime;
    customer.waitTime = customer.startServiceTime - customer.arrivalTime;
    state.totalWaitTime += customer.waitTime;
    
    counter.busy = true;
    counter.customer = customer;
    counter.endTime = state.simTime + customer.serviceTime;
    
    updateCounterDisplay(counter);
}

// Complete service
function completeService(counter) {
    const customer = counter.customer;
    customer.endServiceTime = state.simTime;
    
    counter.busy = false;
    counter.customer = null;
    counter.served++;
    state.completed++;
    
    updateCounterDisplay(counter);
    updateMetrics();
}

// Process queue - try to assign customers to available counters
function processQueue() {
    while (state.queue.length > 0) {
        const counter = findAvailableCounter();
        if (!counter) break;
        
        const customer = state.queue.shift();
        startService(counter, customer);
        updateQueueDisplay();
    }
}

// Check for completed services
function checkServiceCompletion() {
    state.counters.forEach(counter => {
        if (counter.busy && state.simTime >= counter.endTime) {
            completeService(counter);
        }
    });
}

// Update progress bars
function updateProgressBars() {
    state.counters.forEach((counter, index) => {
        const el = elements.counters[index];
        const progressFill = el.querySelector('.progress-fill');
        
        if (counter.busy && counter.customer) {
            const elapsed = state.simTime - counter.customer.startServiceTime;
            const total = counter.customer.serviceTime;
            const percent = Math.min(100, (elapsed / total) * 100);
            progressFill.style.width = percent + '%';
        } else {
            progressFill.style.width = '0%';
        }
    });
}

// UI Update Functions
function updateQueueDisplay() {
    elements.queueDisplay.innerHTML = state.queue.slice(0, 8).map(c => 
        `<div class="queue-customer">C${c.id}</div>`
    ).join('');
    
    if (state.queue.length > 8) {
        elements.queueDisplay.innerHTML += `<div class="queue-customer">+${state.queue.length - 8} more</div>`;
    }
    
    elements.queueLength.textContent = state.queue.length;
}

function updateCounterDisplay(counter) {
    const el = elements.counters[counter.id - 1];
    const statusEl = el.querySelector('.counter-status');
    const customerEl = el.querySelector('.counter-customer');
    
    if (counter.busy) {
        el.classList.add('active');
        statusEl.textContent = 'Busy';
        statusEl.className = 'counter-status busy';
        customerEl.textContent = `C${counter.customer.id}`;
    } else {
        el.classList.remove('active');
        statusEl.textContent = 'Idle';
        statusEl.className = 'counter-status idle';
        customerEl.textContent = '';
    }
}

function updateMetrics() {
    elements.simTime.textContent = state.simTime.toFixed(2) + ' min';
    elements.arrivedCount.textContent = state.customers.length;
    elements.completedCount.textContent = state.completed;
    
    if (state.completed > 0) {
        const avgWait = state.totalWaitTime / state.completed;
        elements.liveAvgWait.textContent = avgWait.toFixed(2) + ' min';
    }
}

// Main simulation tick
function tick() {
    if (!state.running || state.paused) return;
    
    // Advance time
    const timeStep = 0.05 * state.speed;
    state.simTime += timeStep;
    
    // Check for new arrivals
    if (state.simTime >= state.nextArrivalTime) {
        createCustomer();
    }
    
    // Check for completed services
    checkServiceCompletion();
    
    // Process queue
    processQueue();
    
    // Update progress bars
    updateProgressBars();
    
    // Update time display
    elements.simTime.textContent = state.simTime.toFixed(2) + ' min';
    
    // Check end condition
    if (state.simTime >= config.maxSimTime && state.queue.length === 0 && !state.counters.some(c => c.busy)) {
        stopSimulation();
        return;
    }
    
    // Schedule next tick
    setTimeout(tick, config.tickInterval);
}

// Control Functions
function startSimulation() {
    if (state.running && state.paused) {
        state.paused = false;
        elements.startBtn.textContent = '▶ Running...';
        tick();
        return;
    }
    
    state.running = true;
    state.paused = false;
    elements.startBtn.textContent = '▶ Running...';
    elements.startBtn.disabled = true;
    
    scheduleNextArrival();
    tick();
}

function pauseSimulation() {
    state.paused = !state.paused;
    elements.pauseBtn.textContent = state.paused ? '▶ Resume' : '⏸ Pause';
    elements.startBtn.textContent = state.paused ? '▶ Resume' : '▶ Running...';
    elements.startBtn.disabled = !state.paused;
    
    if (!state.paused) {
        tick();
    }
}

function stopSimulation() {
    state.running = false;
    state.paused = false;
    elements.startBtn.textContent = '✓ Complete';
    elements.startBtn.disabled = true;
    elements.pauseBtn.disabled = true;
}

function resetSimulation() {
    state.running = false;
    state.paused = false;
    state.simTime = 0;
    state.customers = [];
    state.queue = [];
    state.counters.forEach(c => {
        c.busy = false;
        c.customer = null;
        c.endTime = 0;
        c.served = 0;
    });
    state.completed = 0;
    state.totalWaitTime = 0;
    state.nextCustomerId = 1;
    state.nextArrivalTime = 0;
    
    // Reset UI
    elements.startBtn.textContent = '▶ Start Simulation';
    elements.startBtn.disabled = false;
    elements.pauseBtn.textContent = '⏸ Pause';
    elements.pauseBtn.disabled = false;
    elements.queueDisplay.innerHTML = '';
    elements.queueLength.textContent = '0';
    elements.completedCount.textContent = '0';
    elements.simTime.textContent = '0.00 min';
    elements.arrivedCount.textContent = '0';
    elements.liveAvgWait.textContent = '0.00 min';
    
    state.counters.forEach((c, i) => updateCounterDisplay(c));
    elements.counters.forEach(el => {
        el.querySelector('.progress-fill').style.width = '0%';
    });
}

// Event Listeners
elements.startBtn.addEventListener('click', startSimulation);
elements.pauseBtn.addEventListener('click', pauseSimulation);
elements.resetBtn.addEventListener('click', resetSimulation);
elements.speedSlider.addEventListener('input', (e) => {
    state.speed = parseInt(e.target.value);
});

// Tab functionality for visualizations
document.querySelectorAll('.viz-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active from all tabs
        document.querySelectorAll('.viz-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.viz-panel').forEach(p => p.classList.remove('active'));
        
        // Add active to clicked tab
        tab.classList.add('active');
        const panelId = 'panel-' + tab.dataset.tab;
        document.getElementById(panelId).classList.add('active');
    });
});

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Animate counter bars on scroll
const observerOptions = {
    threshold: 0.5
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.querySelectorAll('.bar-fill').forEach(bar => {
                bar.style.width = bar.parentElement.parentElement.querySelector('.counter-percent').textContent;
            });
        }
    });
}, observerOptions);

const counterMetrics = document.querySelector('.counter-metrics');
if (counterMetrics) {
    observer.observe(counterMetrics);
}

console.log('🛒 Supermarket Queue Simulation loaded!');

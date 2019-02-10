
// Global parameters

height = 400;
width = 1000;

number_of_layers = 5;
number_of_samples_per_layer = 200;
number_of_bumps_per_layer = 20;

// Test data generators

function bump(a, n) {
    const x = 1 / (0.1 + Math.random());
    const y = 2 * Math.random() - 0.5;
    const z = 10 / (0.1 + Math.random());
    for (let i = 0; i < n; ++i) {
        const w = (i / n - y) * z;
        a[i] += x * Math.exp(-w * w);
    }
}
function bumps(samples_per_layer, bumps_per_layer) {
    const a = [];
    for (let i = 0; i < samples_per_layer; ++i) a[i] = 0;
    for (let i = 0; i < bumps_per_layer; ++i) bump(a, samples_per_layer);
    return a;
}

// Draw stream graph

const svg = d3.select('svg');

const x = d3.scaleLinear()
    .domain([0, number_of_samples_per_layer - 1])
    .range([0, width]);

const y = d3.scaleLinear()
    .range([height, 0]);

const z = d3.interpolateViridis;

const area = d3.area()
    .x((d, i) => x(i))
    .y0(d => y(d[0]))
    .y1(d => y(d[1]));



function set_stack_data() {
    
    stack = d3.stack()
        .keys(d3.range(number_of_layers))
        .order(d3.stackOrderNone)
        .offset(d3.stackOffsetWiggle);

    // bumps functions return randomized data, and should be replaced with fetched data from server
    
    const layersArray = Array.from({ length: number_of_layers }, () => bumps(number_of_samples_per_layer, number_of_bumps_per_layer));
    const layers = stack(d3.transpose(layersArray));

    y.domain([
        d3.min(layers, l => d3.min(l, d => d[0])),
        d3.max(layers, l => d3.max(l, d => d[1]))
    ]);
    
    return layers;
}

const path = svg.selectAll("path")
    .data(set_stack_data)
    .enter().append("path")
    .attr("d", area)
    .attr("fill", () => z(Math.random()));


/**
 * Pathfinding Example
 * Demonstrates graph algorithms for finding shortest paths
 */

import { Graph, dijkstra, bellmanFord, bfs } from '../src/graph.js';

console.log('=== PATHFINDING EXAMPLE ===\n');

// Create a graph representing a city map
const cityMap = new Graph(false); // undirected graph

// Add locations (vertices)
const locations = ['Home', 'School', 'Park', 'Store', 'Library', 'Restaurant', 'Hospital'];
locations.forEach(loc => cityMap.addVertex(loc));

// Add roads (edges) with distances in km
cityMap.addEdge('Home', 'School', 5);
cityMap.addEdge('Home', 'Park', 2);
cityMap.addEdge('Home', 'Store', 3);
cityMap.addEdge('School', 'Library', 1);
cityMap.addEdge('School', 'Hospital', 4);
cityMap.addEdge('Park', 'Restaurant', 3);
cityMap.addEdge('Store', 'Restaurant', 2);
cityMap.addEdge('Store', 'Hospital', 6);
cityMap.addEdge('Library', 'Hospital', 2);
cityMap.addEdge('Restaurant', 'Hospital', 5);

console.log('City Map Created:');
console.log('Locations:', locations.join(', '));
console.log('\n');

// Find shortest path from Home to Hospital using Dijkstra
console.log('Finding shortest path from Home to Hospital...\n');

const result = dijkstra(cityMap, 'Home');
const pathToHospital = result.getPath('Hospital');
const distanceToHospital = result.distances.get('Hospital');

console.log('Shortest path:', pathToHospital.join(' → '));
console.log('Total distance:', distanceToHospital, 'km');

// Find shortest paths from Home to all locations
console.log('\n--- Distances from Home to all locations ---');
for (const loc of locations) {
    if (loc !== 'Home') {
        const path = result.getPath(loc);
        const distance = result.distances.get(loc);
        console.log(`To ${loc}: ${distance} km via [${path.join(' → ')}]`);
    }
}

// Create a delivery route graph with traffic weights
console.log('\n\n=== DELIVERY ROUTE OPTIMIZATION ===\n');

const deliveryMap = new Graph(true); // directed graph for one-way streets

// Add intersections
const intersections = ['A', 'B', 'C', 'D', 'E', 'F'];
intersections.forEach(i => deliveryMap.addVertex(i));

// Add routes with time in minutes (accounting for traffic)
deliveryMap.addEdge('A', 'B', 10);
deliveryMap.addEdge('A', 'C', 15);
deliveryMap.addEdge('B', 'D', 12);
deliveryMap.addEdge('B', 'E', 15);
deliveryMap.addEdge('C', 'B', 7);
deliveryMap.addEdge('C', 'E', 10);
deliveryMap.addEdge('D', 'E', 2);
deliveryMap.addEdge('D', 'F', 5);
deliveryMap.addEdge('E', 'F', 5);

// Sometimes there's construction causing delays (negative edge for testing)
// deliveryMap.addEdge('C', 'D', -5); // Shortcut through construction zone

console.log('Delivery Network Created');
console.log('Finding optimal delivery routes from warehouse A...\n');

const deliveryResult = dijkstra(deliveryMap, 'A');

// Show delivery times to all destinations
console.log('--- Delivery times from Warehouse A ---');
for (const dest of intersections) {
    if (dest !== 'A') {
        const path = deliveryResult.getPath(dest);
        const time = deliveryResult.distances.get(dest);
        if (time !== Infinity) {
            console.log(`To point ${dest}: ${time} minutes via [${path.join(' → ')}]`);
        } else {
            console.log(`To point ${dest}: No route available`);
        }
    }
}

// Find connected components (for network analysis)
console.log('\n\n=== SOCIAL NETWORK ANALYSIS ===\n');

const socialNetwork = new Graph(false); // undirected for friendships

// Add people
const people = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace'];
people.forEach(p => socialNetwork.addVertex(p));

// Add friendships
socialNetwork.addEdge('Alice', 'Bob', 1);
socialNetwork.addEdge('Alice', 'Charlie', 1);
socialNetwork.addEdge('Bob', 'Diana', 1);
socialNetwork.addEdge('Charlie', 'Diana', 1);
socialNetwork.addEdge('Eve', 'Frank', 1);
socialNetwork.addEdge('Frank', 'Grace', 1);

console.log('Social Network Created');
console.log('Finding friend groups...\n');

// Use BFS to find connected components
const visited = new Set();
const groups = [];

for (const person of people) {
    if (!visited.has(person)) {
        const group = bfs(socialNetwork, person);
        group.forEach(p => visited.add(p));
        groups.push(group);
    }
}

console.log(`Found ${groups.length} friend group(s):`);
groups.forEach((group, i) => {
    console.log(`Group ${i + 1}: ${group.join(', ')}`);
});

// Find degrees of separation
console.log('\n--- Degrees of Separation ---');
const aliceDistances = dijkstra(socialNetwork, 'Alice');
for (const person of people) {
    if (person !== 'Alice') {
        const distance = aliceDistances.distances.get(person);
        if (distance !== Infinity) {
            console.log(`Alice to ${person}: ${distance} degree(s) of separation`);
        } else {
            console.log(`Alice and ${person} are not connected`);
        }
    }
}

console.log('\n=== Example completed successfully ===');
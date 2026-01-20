# 📚 Web & Mobile Development - Complete Course Summary

**Module:** Web and Mobile Development  
**Professor:** K. BENCHERIF (k.bencherif@esi-sba.dz)  
**Institution:** ESI-SBA (École Supérieure d'Informatique de Sidi Bel Abbes)  
**Year:** 2025/2026  
**Evaluation:** Exam 60% | CC 40% | Credits: 2 | Coefficient: 2

---

## 📖 Table of Contents
1. [Chapter 1: Introduction to Web Development](#chapter-1-introduction-to-web-development)
2. [Chapter 2: HTML5](#chapter-2-html5)
3. [Chapter 3: CSS3](#chapter-3-css3)
4. [Chapter 4: JavaScript & React](#chapter-4-javascript--react)
5. [Chapter 5: Flutter](#chapter-5-flutter)
6. [Chapter 6: Node.js & NestJS](#chapter-6-nodejs--nestjs)

---

# Chapter 1: Introduction to Web Development

## Course Objectives
- Build responsive and interactive user interfaces using HTML, CSS and JavaScript
- Learn advanced front-end development with ReactJS
- Explore Node.js to develop REST APIs
- Introduce mobile application development with Flutter

## Course Structure
| Topic | Hours |
|-------|-------|
| Introduction | 1h30 |
| HTML5 | 3h |
| CSS3 | 3h |
| JavaScript & ReactJS | 6h |
| Node.js | 3h |
| Mobile Development (Flutter) | 3h |

## Web Application Architecture

### How the Web Works
```
End User → DNS Server → Web Server → Database Server
              ↓
    IP Resolution (e.g., www.esi-sba.dz → 193.194.79.194)
              ↓
    HTTP Request/Response Cycle
```

### Static vs Dynamic Architecture
- **Static:** Server sends pre-made HTML files directly to client
- **Dynamic:** Server processes request, queries database, generates HTML dynamically

## Front-end vs Back-end

### Front-end (Client-side)
- **Languages:** HTML, CSS, JavaScript
- **Frameworks:** React, Angular, Vue.js
- **Purpose:** User interface, what users see and interact with

### Back-end (Server-side)
- **Languages:** JavaScript (Node.js), Python, PHP, Java, Ruby
- **Frameworks:** Express, NestJS, Django, Laravel
- **Purpose:** Server logic, database operations, business logic

## HTTP Protocol

### HTTP Request Methods
| Method | Action | Use Case |
|--------|--------|----------|
| `GET` | Retrieve data | Access web pages, fetch data |
| `POST` | Send data | Submit forms, upload files |
| `PUT` | Update data | Modify existing resources |
| `DELETE` | Remove data | Delete resources |
| `HEAD` | Get headers only | Check resource metadata |
| `CONNECT` | Establish tunnel | Connect to proxy servers |

### HTTP Response Status Codes
| Code Range | Category | Examples |
|------------|----------|----------|
| 1xx | Information | 100 Continue |
| 2xx | Success | 200 OK, 201 Created |
| 3xx | Redirection | 301 Moved, 302 Found |
| 4xx | Client Error | 400 Bad Request, 404 Not Found, 403 Forbidden |
| 5xx | Server Error | 500 Internal Server Error, 503 Service Unavailable |

## Development Tools
- **Code Editors:** VS Code, Sublime Text, Atom
- **Web Servers:** Apache, Nginx, Node.js
- **Browsers:** Chrome, Firefox, Edge (with DevTools)

---

# Chapter 2: HTML5

## HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
</head>
<body>
    <!-- Content here -->
</body>
</html>
```

## Forms

### Form Tag Syntax
```html
<form method="POST|GET" action="/submit-url" name="formName">
    <!-- form controls -->
</form>
```

- **method:** How data is sent (GET or POST)
- **action:** URL that receives the data
- **name:** Form identifier

### GET vs POST Methods
| GET | POST |
|-----|------|
| Data appended to URL | Data in request body |
| Visible in browser address bar | Hidden from URL |
| Use for non-sensitive data | Use for sensitive data |
| Can be bookmarked | Cannot be bookmarked |
| Limited data size (~2048 chars) | No size limit |

### Input Types
| Type | Description | Example |
|------|-------------|---------|
| `text` | Single-line text | `<input type="text">` |
| `password` | Hidden text | `<input type="password">` |
| `email` | Email validation | `<input type="email">` |
| `number` | Numeric input | `<input type="number" min="0" max="100">` |
| `date` | Date picker | `<input type="date">` |
| `checkbox` | Multiple selections | `<input type="checkbox">` |
| `radio` | Single selection | `<input type="radio">` |
| `file` | File upload | `<input type="file">` |
| `hidden` | Hidden field | `<input type="hidden">` |
| `submit` | Submit button | `<input type="submit">` |
| `range` | Slider | `<input type="range">` |
| `color` | Color picker | `<input type="color">` |
| `tel` | Phone number | `<input type="tel">` |
| `url` | URL input | `<input type="url">` |

### Input Attributes
| Attribute | Description |
|-----------|-------------|
| `autofocus` | Automatically focus on page load |
| `placeholder` | Hint text inside input |
| `size` | Visible width (characters) |
| `maxlength` | Maximum characters allowed |
| `minlength` | Minimum characters required |
| `readonly` | Cannot be edited |
| `disabled` | Disabled (not sent to server) |
| `required` | Must be filled |
| `pattern` | Regular expression validation |
| `min` / `max` | Value range for numbers/dates |
| `value` | Default/current value |
| `name` | Field identifier (sent to server) |
| `id` | Unique identifier for CSS/JS |

### Form Validation
```html
<!-- Required field with pattern -->
<input type="text" name="username" 
       required 
       pattern="[a-zA-Z0-9]+" 
       placeholder="Username"
       minlength="3" 
       maxlength="20">

<!-- Email validation -->
<input type="email" name="email" required>

<!-- Number range -->
<input type="number" name="age" min="18" max="99">

<!-- Disable HTML5 validation -->
<form novalidate>...</form>
```

### Other Form Elements
```html
<!-- Textarea (multi-line) -->
<textarea name="message" rows="5" cols="30"></textarea>

<!-- Dropdown -->
<select name="country">
    <optgroup label="Europe">
        <option value="fr">France</option>
        <option value="de">Germany</option>
    </optgroup>
</select>

<!-- Label (accessibility) -->
<label for="email">Email:</label>
<input type="email" id="email" name="email">

<!-- Fieldset with legend -->
<fieldset>
    <legend>Personal Info</legend>
    <!-- inputs here -->
</fieldset>
```

## Tables
```html
<table>
    <caption>Student Grades</caption>
    <thead>
        <tr>
            <th>Name</th>
            <th>Grade</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Ali</td>
            <td>18</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="2">Average: 16.5</td>
        </tr>
    </tfoot>
</table>
```

## HTML5 APIs

### Geolocation
```javascript
navigator.geolocation.getCurrentPosition(
    function(position) {
        console.log("Latitude:", position.coords.latitude);
        console.log("Longitude:", position.coords.longitude);
    },
    function(error) {
        console.log("Error:", error.message);
    }
);

// Continuous tracking
navigator.geolocation.watchPosition(callback);
```

### Google Maps Integration
```html
<div id="map"></div>
<script>
function initMap() {
    var myLatLng = {lat: 35.2, lng: -0.641389};
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 4
    });
    var marker = new google.maps.Marker({
        map: map,
        position: myLatLng
    });
}
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=initMap" async defer></script>
```

### Drag and Drop
```html
<img id="drag1" src="img.jpg" draggable="true" ondragstart="drag(event)">
<div id="dropZone" ondrop="drop(event)" ondragover="allowDrop(event)"></div>

<script>
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}
</script>
```

### WebSocket (Real-time Communication)
```javascript
const socket = new WebSocket("wss://example.com/socket");

socket.onopen = () => console.log("Connected");
socket.onmessage = (event) => console.log("Received:", event.data);
socket.onerror = (error) => console.log("Error:", error);
socket.onclose = () => console.log("Disconnected");

// Send message
socket.send("Hello, server!");
```

### WebRTC (Peer-to-Peer)
```javascript
var video = document.getElementById("video");
navigator.mediaDevices.getUserMedia({video: true, audio: true})
    .then(function(stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function(error) {
        console.log("Error:", error);
    });
```

### Canvas (2D Graphics)
```html
<canvas id="myCanvas" width="400" height="300"></canvas>
<script>
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// Rectangle
ctx.fillStyle = "blue";
ctx.fillRect(10, 10, 100, 50);

// Circle
ctx.beginPath();
ctx.arc(200, 100, 40, 0, 2 * Math.PI);
ctx.fill();

// Line
ctx.moveTo(0, 0);
ctx.lineTo(200, 100);
ctx.stroke();
</script>
```

### Web Storage
```javascript
// localStorage (persists after browser close)
localStorage.setItem("username", "ali");
let user = localStorage.getItem("username");
localStorage.removeItem("username");
localStorage.clear();

// sessionStorage (cleared when tab closes)
sessionStorage.setItem("temp", "data");
```

---

# Chapter 3: CSS3

## CSS Syntax
```css
selector {
    property: value;
    property2: value2;
}
```

## CSS Inclusion Methods
```html
<!-- 1. Inline (in HTML element) -->
<p style="color: red;">Text</p>

<!-- 2. Internal (in <head>) -->
<style>
    p { color: red; }
</style>

<!-- 3. External (separate file) -->
<link rel="stylesheet" href="styles.css">
```

## Selectors

### Basic Selectors
```css
/* Element selector */
p { color: blue; }

/* Class selector (.) */
.highlight { background: yellow; }

/* ID selector (#) - must be unique */
#header { font-size: 24px; }

/* Universal selector */
* { margin: 0; padding: 0; }
```

### Hierarchy Selectors
```css
/* Descendant (any level) */
div p { color: red; }

/* Direct child (>) */
div > p { color: blue; }

/* Adjacent sibling (+) */
h1 + p { margin-top: 0; }

/* General sibling (~) */
h1 ~ p { color: gray; }
```

### Attribute Selectors
```css
input[type="text"] { border: 1px solid black; }
a[href^="https"] { color: green; }  /* starts with */
a[href$=".pdf"] { color: red; }     /* ends with */
a[href*="example"] { color: blue; } /* contains */
```

### Pseudo-classes
```css
a:hover { color: red; }
a:visited { color: purple; }
input:focus { border-color: blue; }
li:first-child { font-weight: bold; }
li:last-child { border: none; }
li:nth-child(odd) { background: #f0f0f0; }
li:nth-child(2n+1) { background: #f0f0f0; }
```

## Display Property

| Value | Description |
|-------|-------------|
| `block` | Full width, new line before/after |
| `inline` | Only needed width, no new line |
| `inline-block` | Inline with block properties |
| `none` | Hidden, removed from flow |
| `flex` | Flexbox container |
| `grid` | Grid container |

## Position Property

### Position Values
| Value | Description |
|-------|-------------|
| `static` | Default, normal document flow |
| `relative` | Relative to original position, space preserved |
| `absolute` | Removed from flow, relative to positioned ancestor |
| `fixed` | Fixed to viewport, stays on scroll |
| `sticky` | Switches between relative and fixed |

### Examples
```css
/* Relative positioning */
.box {
    position: relative;
    top: 10px;
    left: 20px;
}

/* Absolute positioning */
.popup {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* Fixed header */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
}

/* Sticky element */
.sidebar {
    position: sticky;
    top: 20px;
}
```

## Flexbox

### Container Properties
```css
.container {
    display: flex;
    
    /* Main axis direction */
    flex-direction: row | row-reverse | column | column-reverse;
    
    /* Wrapping */
    flex-wrap: nowrap | wrap | wrap-reverse;
    
    /* Main axis alignment */
    justify-content: flex-start | flex-end | center | space-between | space-around | space-evenly;
    
    /* Cross axis alignment */
    align-items: flex-start | flex-end | center | stretch | baseline;
    
    /* Multi-line cross axis */
    align-content: flex-start | flex-end | center | stretch | space-between | space-around;
    
    /* Gap between items */
    gap: 10px;
}
```

### Item Properties
```css
.item {
    /* Growth ratio */
    flex-grow: 0;  /* default, don't grow */
    flex-grow: 1;  /* grow equally */
    
    /* Shrink ratio */
    flex-shrink: 1;  /* default, can shrink */
    flex-shrink: 0;  /* don't shrink */
    
    /* Initial size */
    flex-basis: auto | 200px | 50%;
    
    /* Shorthand */
    flex: 1;  /* flex-grow: 1, flex-shrink: 1, flex-basis: 0 */
    
    /* Individual alignment */
    align-self: auto | flex-start | flex-end | center | stretch;
    
    /* Order */
    order: 0;  /* default */
}
```

### Common Flexbox Patterns
```css
/* Centered content */
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

/* Navigation bar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Equal columns */
.columns {
    display: flex;
}
.column {
    flex: 1;
}

/* Card grid */
.cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.card {
    flex: 1 1 300px;  /* grow, shrink, min-width */
}
```

## Media Queries (Responsive Design)

### Syntax
```css
@media media-type and (condition) {
    /* styles */
}
```

### Media Types
| Type | Description |
|------|-------------|
| `screen` | Monitors, tablets, phones |
| `print` | Print preview and printing |
| `all` | All devices (default) |
| `speech` | Screen readers |

### Features/Conditions
| Feature | Description |
|---------|-------------|
| `width` / `height` | Viewport dimensions |
| `min-width` / `max-width` | Minimum/maximum width |
| `orientation` | `portrait` or `landscape` |
| `resolution` | Screen pixel density |
| `prefers-color-scheme` | `light` or `dark` |
| `prefers-reduced-motion` | Accessibility preference |

### Logical Operators
| Operator | Description |
|----------|-------------|
| `and` | Both conditions must be true |
| `,` (comma) | OR - any condition can be true |
| `not` | Negates the query |
| `only` | Applies only if exact match |

### Responsive Breakpoints
```css
/* Mobile first approach */

/* Base styles (mobile) */
.container {
    width: 100%;
    padding: 10px;
}

/* Small tablets (576px+) */
@media screen and (min-width: 576px) {
    .container { max-width: 540px; }
}

/* Tablets (768px+) */
@media screen and (min-width: 768px) {
    .container { max-width: 720px; }
}

/* Laptops (992px+) */
@media screen and (min-width: 992px) {
    .container { max-width: 960px; }
}

/* Desktops (1200px+) */
@media screen and (min-width: 1200px) {
    .container { max-width: 1140px; }
}

/* Range query */
@media screen and (min-width: 400px) and (max-width: 700px) {
    body { background-color: lightblue; }
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    body { background: #1a1a1a; color: white; }
}
```

### Print Styles
```css
@media print {
    /* Hide navigation */
    nav, .no-print { display: none; }
    
    /* Black text */
    body { color: black; }
    
    /* Show links */
    a[href]::after { content: " (" attr(href) ")"; }
    
    /* Page breaks */
    h1 { page-break-before: always; }
}
```

---

# Chapter 4: JavaScript & React

## JavaScript Basics

### Variables
```javascript
// Modern (use these)
let name = "Ali";        // can be reassigned
const age = 25;          // cannot be reassigned

// Legacy (avoid)
var oldStyle = "avoid";
```

### Data Types
```javascript
// Primitives
let string = "Hello";
let number = 42;
let boolean = true;
let nullValue = null;
let undefinedValue = undefined;

// Objects
let object = { name: "Ali", age: 25 };
let array = [1, 2, 3, 4, 5];
let func = function() { return "hello"; };
```

### Functions
```javascript
// Function declaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Function expression
const greet = function(name) {
    return `Hello, ${name}!`;
};

// Arrow function (ES6)
const greet = (name) => `Hello, ${name}!`;

// Arrow with multiple statements
const calculate = (a, b) => {
    const sum = a + b;
    return sum * 2;
};
```

### Array Methods
```javascript
const numbers = [1, 2, 3, 4, 5];

// map - transform each element
const doubled = numbers.map(n => n * 2);  // [2, 4, 6, 8, 10]

// filter - keep elements that pass test
const evens = numbers.filter(n => n % 2 === 0);  // [2, 4]

// reduce - accumulate to single value
const sum = numbers.reduce((acc, n) => acc + n, 0);  // 15

// find - first element that passes test
const found = numbers.find(n => n > 3);  // 4

// forEach - iterate (no return)
numbers.forEach(n => console.log(n));

// some - at least one passes
const hasEven = numbers.some(n => n % 2 === 0);  // true

// every - all pass
const allPositive = numbers.every(n => n > 0);  // true

// includes - check if exists
const hasThree = numbers.includes(3);  // true
```

### Object Destructuring
```javascript
const user = { name: "Ali", age: 25, city: "Algiers" };

// Destructuring
const { name, age } = user;

// With alias
const { name: userName } = user;

// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
```

### Spread Operator
```javascript
// Arrays
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];  // [1, 2, 3, 4, 5]

// Objects
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };  // { a: 1, b: 2, c: 3 }
```

## DOM Manipulation

### Selecting Elements
```javascript
// By ID
const element = document.getElementById("myId");

// By class
const elements = document.getElementsByClassName("myClass");

// By tag
const divs = document.getElementsByTagName("div");

// Query selector (returns first match)
const first = document.querySelector(".myClass");
const input = document.querySelector("input[type='text']");

// Query all (returns NodeList)
const all = document.querySelectorAll(".myClass");
```

### Modifying Elements
```javascript
// Content
element.textContent = "New text";
element.innerHTML = "<strong>Bold</strong>";

// Attributes
element.setAttribute("class", "active");
element.getAttribute("id");
element.removeAttribute("disabled");

// Styles
element.style.color = "red";
element.style.backgroundColor = "blue";

// Classes
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("visible");
element.classList.contains("active");
```

### Events
```javascript
// Add event listener
element.addEventListener("click", function(event) {
    console.log("Clicked!", event.target);
});

// Common events
// click, dblclick, mouseenter, mouseleave
// keydown, keyup, keypress
// submit, change, input, focus, blur
// load, DOMContentLoaded, scroll, resize

// Event object
element.addEventListener("click", (e) => {
    e.preventDefault();   // prevent default action
    e.stopPropagation(); // stop bubbling
    e.target;            // element that triggered
    e.currentTarget;     // element listener attached to
});
```

## React

### What is React?
- Component-based library for building UIs
- Uses Virtual DOM for efficient updates
- Declarative syntax (describe what you want, not how)
- Large ecosystem and community

### Why Use React?
- **Component-based:** Reusable UI blocks
- **Virtual DOM:** Faster rendering
- **Declarative:** Easier to understand
- **Cross-platform:** Web, mobile (React Native), desktop

### Installing React
```bash
npx create-react-app my-app
cd my-app
npm start
# Opens http://localhost:3000
```

### Project Structure
```
my-app/
├── node_modules/     # Dependencies
├── public/           # Static files
│   └── index.html
├── src/              # React code
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json      # Configuration
└── README.md
```

### JSX (JavaScript XML)
```jsx
// JSX allows HTML-like syntax in JavaScript
function Welcome() {
    return (
        <div>
            <h1>Welcome to React!</h1>
            <p>JSX makes coding intuitive.</p>
        </div>
    );
}

// JSX is compiled to:
React.createElement('div', null,
    React.createElement('h1', null, 'Welcome to React!'),
    React.createElement('p', null, 'JSX makes coding intuitive.')
);
```

### JSX Rules
1. **Return single parent element** (use `<div>` or `<>`)
2. **Use `className` instead of `class`**
3. **Close all tags** (`<img />`, `<br />`)
4. **Use `{}` for JavaScript expressions**

### Embedding JavaScript in JSX
```jsx
const name = "Mohamed";
const isLoggedIn = true;

function App() {
    return (
        <div>
            {/* Variables */}
            <h1>Hello, {name}!</h1>
            
            {/* Expressions */}
            <p>2 + 2 = {2 + 2}</p>
            
            {/* Conditional rendering */}
            {isLoggedIn && <p>Welcome back!</p>}
            {isLoggedIn ? <LogoutBtn /> : <LoginBtn />}
            
            {/* Lists */}
            {items.map(item => <li key={item.id}>{item.name}</li>)}
        </div>
    );
}
```

### Components

#### Functional Components (Modern)
```jsx
// Simple component
function Welcome() {
    return <h1>Hello, React!</h1>;
}

// Arrow function
const Welcome = () => {
    return <h1>Hello, React!</h1>;
};

// With props
function Greeting({ name, age }) {
    return (
        <div>
            <h1>Hello, {name}!</h1>
            <p>You are {age} years old.</p>
        </div>
    );
}
```

#### Class Components (Legacy)
```jsx
class Welcome extends React.Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

### Props (Properties)
```jsx
// Parent passes props
function App() {
    return (
        <div>
            <Student name="Ali" age={20} />
            <Student name="Sara" age={22} />
        </div>
    );
}

// Child receives props
function Student({ name, age }) {
    return (
        <div>
            <h2>{name}</h2>
            <p>Age: {age}</p>
        </div>
    );
}

// Props are read-only!
```

### Events in React
```jsx
function App() {
    // Event handler
    function handleClick() {
        alert("Button clicked!");
    }
    
    // With parameter
    function handleGreet(name) {
        alert(`Hello, ${name}!`);
    }
    
    return (
        <div>
            {/* Simple handler */}
            <button onClick={handleClick}>Click me</button>
            
            {/* With parameter */}
            <button onClick={() => handleGreet("Ali")}>Greet Ali</button>
            
            {/* Inline handler */}
            <button onClick={() => console.log("Clicked!")}>Log</button>
        </div>
    );
}
```

### Hooks

#### useState - State Management
```jsx
import { useState } from 'react';

function Counter() {
    // Declare state: [value, setter] = useState(initialValue)
    const [count, setCount] = useState(0);
    const [name, setName] = useState("");
    const [items, setItems] = useState([]);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(prev => prev - 1)}>-1</button>
            <button onClick={() => setCount(0)}>Reset</button>
            
            <input 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
            />
        </div>
    );
}
```

#### useEffect - Side Effects
```jsx
import { useState, useEffect } from 'react';

function DataFetcher() {
    const [data, setData] = useState(null);
    
    // Run on mount only
    useEffect(() => {
        fetch('/api/data')
            .then(res => res.json())
            .then(data => setData(data));
    }, []);  // Empty array = run once
    
    // Run when dependency changes
    useEffect(() => {
        console.log("Count changed:", count);
    }, [count]);
    
    // Cleanup on unmount
    useEffect(() => {
        const timer = setInterval(() => console.log("tick"), 1000);
        return () => clearInterval(timer);  // Cleanup
    }, []);
    
    return <div>{data ? data.name : "Loading..."}</div>;
}
```

#### Other Hooks
| Hook | Purpose |
|------|---------|
| `useContext` | Access context values |
| `useReducer` | Complex state logic |
| `useRef` | Mutable reference, DOM access |
| `useMemo` | Cache expensive calculations |
| `useCallback` | Cache functions |

### Custom Hooks
```jsx
// Create reusable logic
function useCounter(initialValue = 0) {
    const [count, setCount] = useState(initialValue);
    
    const increment = () => setCount(c => c + 1);
    const decrement = () => setCount(c => c - 1);
    const reset = () => setCount(initialValue);
    
    return { count, increment, decrement, reset };
}

// Use it
function MyComponent() {
    const { count, increment, decrement } = useCounter(10);
    
    return (
        <div>
            <p>{count}</p>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
        </div>
    );
}
```

### Styling in React

#### 1. Inline Styles
```jsx
<div style={{ color: 'red', padding: '20px' }}>
    Styled div
</div>
```

#### 2. External CSS
```jsx
// App.css
.container {
    padding: 20px;
}

// App.js
import './App.css';
<div className="container">Content</div>
```

#### 3. CSS Modules (Scoped)
```jsx
// Button.module.css
.button {
    padding: 10px 20px;
}

// Button.js
import styles from './Button.module.css';
<button className={styles.button}>Click</button>
```

### Context API (Global State)
```jsx
import { createContext, useContext, useState } from 'react';

// Create context
const ThemeContext = createContext();

// Provider component
function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    
    const toggleTheme = () => {
        setTheme(t => t === 'light' ? 'dark' : 'light');
    };
    
    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

// Use context in any component
function Header() {
    const { theme, toggleTheme } = useContext(ThemeContext);
    
    return (
        <header className={theme}>
            <button onClick={toggleTheme}>Toggle Theme</button>
        </header>
    );
}

// App setup
function App() {
    return (
        <ThemeProvider>
            <Header />
            <Main />
        </ThemeProvider>
    );
}
```

### React Router (Navigation)
```jsx
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            {/* Navigation */}
            <nav>
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
                <Link to="/users/123">User 123</Link>
            </nav>
            
            {/* Routes */}
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/users/:id" element={<UserDetail />} />
            </Routes>
        </BrowserRouter>
    );
}

// Programmatic navigation
function LoginForm() {
    const navigate = useNavigate();
    
    const handleSubmit = () => {
        // After login...
        navigate('/dashboard');
    };
}
```

---

# Chapter 5: Flutter

## Introduction to Flutter
- Cross-platform framework by Google
- Single codebase for iOS, Android, Web, Desktop
- Uses Dart programming language
- Everything is a Widget
- Hot reload for fast development

## Widget Basics

### Widget Tree
```
MaterialApp
└── Scaffold
    ├── AppBar
    │   └── Text
    └── body
        └── Center
            └── Column
                ├── Text
                └── ElevatedButton
```

### StatelessWidget
```dart
class MyWidget extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Text("Hello World");
    }
}
```

### StatefulWidget
```dart
class Counter extends StatefulWidget {
    @override
    State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
    int count = 0;
    
    void increment() {
        setState(() {
            count++;
        });
    }
    
    @override
    Widget build(BuildContext context) {
        return Column(
            children: [
                Text('Count: $count'),
                ElevatedButton(
                    onPressed: increment,
                    child: Text('Add'),
                ),
            ],
        );
    }
}
```

### StatefulWidget Lifecycle
1. `createState()` - Creates state object
2. `initState()` - Initialize (called once)
3. `build()` - Build UI (called on every setState)
4. `didUpdateWidget()` - Parent rebuilt
5. `dispose()` - Cleanup (called once)

## Common Widgets

### Scaffold (App Structure)
```dart
Scaffold(
    appBar: AppBar(
        title: Text("My App"),
        actions: [
            IconButton(
                icon: Icon(Icons.search),
                onPressed: () {},
            ),
        ],
    ),
    body: Center(
        child: Text("Hello"),
    ),
    floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: Icon(Icons.add),
    ),
    drawer: Drawer(
        child: ListView(...),
    ),
    bottomNavigationBar: BottomNavigationBar(
        items: [...],
    ),
)
```

### Text & Styling
```dart
Text(
    "Hello World",
    style: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: Colors.blue,
    ),
)
```

### Buttons
```dart
// Elevated Button
ElevatedButton(
    onPressed: () => print("Pressed"),
    child: Text("Click Me"),
)

// Text Button
TextButton(
    onPressed: () {},
    child: Text("Text Button"),
)

// Icon Button
IconButton(
    icon: Icon(Icons.favorite),
    onPressed: () {},
)

// Outlined Button
OutlinedButton(
    onPressed: () {},
    child: Text("Outlined"),
)
```

### Input Widgets
```dart
// TextField
TextField(
    decoration: InputDecoration(
        labelText: "Enter name",
        hintText: "Your name here",
        border: OutlineInputBorder(),
        prefixIcon: Icon(Icons.person),
    ),
    onChanged: (value) => print(value),
)

// TextFormField (with validation)
TextFormField(
    decoration: InputDecoration(labelText: "Email"),
    validator: (value) {
        if (value == null || value.isEmpty) {
            return "Email is required";
        }
        if (!value.contains('@')) {
            return "Invalid email";
        }
        return null;
    },
)

// Checkbox
Checkbox(
    value: isChecked,
    onChanged: (value) {
        setState(() => isChecked = value!);
    },
)

// Radio
Radio<int>(
    value: 1,
    groupValue: selectedValue,
    onChanged: (value) {
        setState(() => selectedValue = value!);
    },
)

// Switch
Switch(
    value: isOn,
    onChanged: (value) {
        setState(() => isOn = value);
    },
)
```

## Layouts

### Container
```dart
Container(
    width: 200,
    height: 100,
    padding: EdgeInsets.all(16),
    margin: EdgeInsets.symmetric(horizontal: 20),
    decoration: BoxDecoration(
        color: Colors.blue,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
            BoxShadow(
                color: Colors.grey,
                blurRadius: 5,
                offset: Offset(2, 2),
            ),
        ],
    ),
    child: Text("Hello"),
)
```

### Row & Column
```dart
// Row (horizontal)
Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
        Text("Left"),
        Text("Center"),
        Text("Right"),
    ],
)

// Column (vertical)
Column(
    mainAxisAlignment: MainAxisAlignment.center,
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
        Text("Top"),
        Text("Middle"),
        Text("Bottom"),
    ],
)
```

### ListView
```dart
// Static list
ListView(
    children: [
        ListTile(title: Text("Item 1")),
        ListTile(title: Text("Item 2")),
        ListTile(title: Text("Item 3")),
    ],
)

// Dynamic list
ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, index) {
        return ListTile(
            title: Text(items[index]),
        );
    },
)
```

### GridView
```dart
GridView.count(
    crossAxisCount: 2,
    children: [
        Card(child: Text("1")),
        Card(child: Text("2")),
        Card(child: Text("3")),
        Card(child: Text("4")),
    ],
)
```

## Navigation

### Navigator.push / pop
```dart
// Navigate to new screen
Navigator.push(
    context,
    MaterialPageRoute(builder: (context) => SecondScreen()),
);

// Go back
Navigator.pop(context);

// Go back with data
Navigator.pop(context, result);
```

### Named Routes
```dart
// Define routes in MaterialApp
MaterialApp(
    initialRoute: '/',
    routes: {
        '/': (context) => HomeScreen(),
        '/details': (context) => DetailsScreen(),
        '/settings': (context) => SettingsScreen(),
    },
)

// Navigate using name
Navigator.pushNamed(context, '/details');

// Pass data
Navigator.pushNamed(
    context,
    '/details',
    arguments: {'id': 123, 'name': 'Product'},
);

// Receive data
final args = ModalRoute.of(context)!.settings.arguments as Map;
```

## Form Validation
```dart
class LoginForm extends StatefulWidget {
    @override
    State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
    final _formKey = GlobalKey<FormState>();
    String _email = '';
    String _password = '';
    
    void _submit() {
        if (_formKey.currentState!.validate()) {
            _formKey.currentState!.save();
            // Process login
            print('Email: $_email, Password: $_password');
        }
    }
    
    @override
    Widget build(BuildContext context) {
        return Form(
            key: _formKey,
            child: Column(
                children: [
                    TextFormField(
                        decoration: InputDecoration(labelText: 'Email'),
                        validator: (value) {
                            if (value == null || value.isEmpty) {
                                return 'Email is required';
                            }
                            return null;
                        },
                        onSaved: (value) => _email = value!,
                    ),
                    TextFormField(
                        decoration: InputDecoration(labelText: 'Password'),
                        obscureText: true,
                        validator: (value) {
                            if (value == null || value.length < 6) {
                                return 'Password must be at least 6 characters';
                            }
                            return null;
                        },
                        onSaved: (value) => _password = value!,
                    ),
                    ElevatedButton(
                        onPressed: _submit,
                        child: Text('Login'),
                    ),
                ],
            ),
        );
    }
}
```

## Advanced Features

### Sensors
| Sensor | Use Case |
|--------|----------|
| Accelerometer | Movement detection, shake |
| Gyroscope | Rotation, VR, games |
| Proximity | Turn off screen during calls |
| Light | Auto brightness |
| GPS | Location, maps |

### Permissions
```dart
// Common permissions
// - Camera
// - Microphone
// - Location
// - Storage
// - Phone

// Add to AndroidManifest.xml
// <uses-permission android:name="android.permission.CAMERA"/>
```

### Background Services
- Music player continuing when app closed
- Location tracking
- Notifications
- Scheduled tasks

### Threads
- **Main Thread:** UI work
- **Background Threads:** Heavy tasks (downloads, parsing, database)

### Room Database
```dart
// Entity
@entity
class User {
    @primaryKey
    final int id;
    final String name;
}

// DAO (Data Access Object)
@dao
abstract class UserDao {
    @Query('SELECT * FROM User')
    Future<List<User>> getAllUsers();
    
    @insert
    Future<void> insertUser(User user);
}

// Database
@Database(version: 1, entities: [User])
abstract class AppDatabase extends FloorDatabase {
    UserDao get userDao;
}
```

---

# Chapter 6: Node.js & NestJS

## Node.js

### What is Node.js?
- JavaScript runtime built on Chrome V8 engine
- Runs JavaScript outside the browser (server-side)
- Created by Ryan Dahl in 2009
- Single-threaded but non-blocking
- Event-driven architecture
- 40% JavaScript, 60% C++

### Why Node.js?
- High performance
- Non-blocking I/O
- Same language for frontend and backend
- Large npm ecosystem
- Great for real-time applications

### Basic Example
```javascript
console.log("Hello, Node.js!");

// Run with: node app.js
```

### NPM (Node Package Manager)
```bash
# Install package
npm install package-name
npm install -g package-name  # globally

# Uninstall
npm uninstall package-name

# Update
npm update package-name

# List installed
npm ls

# Initialize project
npm init
npm init -y  # with defaults
```

### Creating an HTTP Server
```javascript
var http = require('http');
var port = 3000;

var server = http.createServer(function(request, response) {
    // Set response headers
    response.writeHead(200, { 'Content-Type': 'text/html' });
    
    // Write response body
    response.write("<html><body><h1>Hello World!</h1></body></html>");
    
    // End response
    response.end();
});

server.listen(port);
console.log("Server running on port " + port);
```

### Events System
```javascript
var events = require('events');

// Create EventEmitter
var emitter = new events.EventEmitter();

// Add listener
emitter.addListener('userConnected', function(user) {
    console.log('User connected:', user.name);
});

// Shorthand for addListener
emitter.on('message', function(msg) {
    console.log('Message:', msg);
});

// One-time listener
emitter.once('firstConnection', function() {
    console.log('This runs only once');
});

// Emit event
emitter.emit('userConnected', { name: 'Ali', age: 25 });
emitter.emit('message', 'Hello World');

// Remove listener
function handler() { console.log('Handler'); }
emitter.on('test', handler);
emitter.removeListener('test', handler);

// Remove all listeners
emitter.removeAllListeners('test');
```

### Event Methods
| Method | Description |
|--------|-------------|
| `on(event, listener)` | Add listener |
| `addListener(event, listener)` | Same as on |
| `once(event, listener)` | Add one-time listener |
| `emit(event, [args])` | Trigger event |
| `removeListener(event, listener)` | Remove specific listener |
| `removeAllListeners(event)` | Remove all listeners |
| `setMaxListeners(n)` | Set max listeners |
| `listeners(event)` | Get all listeners |

### Inheriting EventEmitter
```javascript
var events = require('events');
var util = require('util');

// Create class
function Server() {
    events.EventEmitter.call(this);
}

// Inherit from EventEmitter
util.inherits(Server, events.EventEmitter);

// Use it
var server = new Server();
server.on('connection', function() {
    console.log('Client connected');
});
server.emit('connection');
```

### Using External Modules
```javascript
// Install: npm install colors
var colors = require('colors');

console.log('Green text'.green);
console.log('Red text'.red);
console.log('Blue background'.bgBlue);
console.log('Bold and yellow'.bold.yellow);
```

## NestJS

### What is NestJS?
- Progressive Node.js framework
- Built with TypeScript (JS compatible)
- Angular-like structure
- Modular architecture
- Built-in dependency injection
- Supports Express/Fastify
- Scalable and maintainable

### Installing NestJS
```bash
# Install CLI globally
npm install -g @nestjs/cli

# Create new project
nest new project-name

# Run project
cd project-name
npm run start

# Development mode (watch)
npm run start:dev
```

### Project Structure
```
src/
├── app.controller.ts    # Controller
├── app.service.ts       # Service
├── app.module.ts        # Module
└── main.ts              # Entry point
```

### Architecture
```
Module
├── Controller (handles requests)
└── Service (business logic)
```

### Modules
```typescript
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
    controllers: [UsersController],
    providers: [UsersService],
    exports: [UsersService],  // Make available to other modules
})
export class UsersModule {}
```

Generate module:
```bash
nest generate module users
# or
nest g mo users
```

### Controllers
```typescript
import { Controller, Get, Post, Put, Delete, Param, Body, Query } from '@nestjs/common';

@Controller('users')  // Route prefix: /users
export class UsersController {
    constructor(private usersService: UsersService) {}
    
    // GET /users
    @Get()
    findAll() {
        return this.usersService.findAll();
    }
    
    // GET /users/:id
    @Get(':id')
    findOne(@Param('id') id: string) {
        return this.usersService.findOne(id);
    }
    
    // GET /users?name=ali
    @Get('search')
    search(@Query('name') name: string) {
        return this.usersService.search(name);
    }
    
    // POST /users
    @Post()
    create(@Body() createUserDto: CreateUserDto) {
        return this.usersService.create(createUserDto);
    }
    
    // PUT /users/:id
    @Put(':id')
    update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
        return this.usersService.update(id, updateUserDto);
    }
    
    // DELETE /users/:id
    @Delete(':id')
    remove(@Param('id') id: string) {
        return this.usersService.remove(id);
    }
}
```

Generate controller:
```bash
nest generate controller users
# or
nest g co users
```

### HTTP Method Decorators
| Decorator | HTTP Method |
|-----------|-------------|
| `@Get()` | GET |
| `@Post()` | POST |
| `@Put()` | PUT |
| `@Patch()` | PATCH |
| `@Delete()` | DELETE |

### Parameter Decorators
| Decorator | Description |
|-----------|-------------|
| `@Param('id')` | Route parameter |
| `@Query('name')` | Query string |
| `@Body()` | Request body |
| `@Headers('auth')` | Request header |
| `@Req()` | Full request object |
| `@Res()` | Response object |

### Services (Providers)
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
    private users = [
        { id: 1, name: 'Ali' },
        { id: 2, name: 'Sara' },
    ];
    
    findAll() {
        return this.users;
    }
    
    findOne(id: string) {
        return this.users.find(u => u.id === parseInt(id));
    }
    
    create(user: CreateUserDto) {
        const newUser = { id: Date.now(), ...user };
        this.users.push(newUser);
        return newUser;
    }
    
    update(id: string, user: UpdateUserDto) {
        const index = this.users.findIndex(u => u.id === parseInt(id));
        this.users[index] = { ...this.users[index], ...user };
        return this.users[index];
    }
    
    remove(id: string) {
        const index = this.users.findIndex(u => u.id === parseInt(id));
        return this.users.splice(index, 1);
    }
}
```

Generate service:
```bash
nest generate service users
# or
nest g s users
```

### Dependency Injection
```typescript
// NestJS automatically injects dependencies
@Controller('users')
export class UsersController {
    // UsersService is automatically injected
    constructor(private usersService: UsersService) {}
    
    @Get()
    findAll() {
        // Use the injected service
        return this.usersService.findAll();
    }
}
```

### DTOs (Data Transfer Objects)
```typescript
// create-user.dto.ts
export class CreateUserDto {
    name: string;
    email: string;
    age: number;
}

// update-user.dto.ts
export class UpdateUserDto {
    name?: string;
    email?: string;
    age?: number;
}
```

### Complete Example
```typescript
// users.module.ts
@Module({
    controllers: [UsersController],
    providers: [UsersService],
})
export class UsersModule {}

// users.service.ts
@Injectable()
export class UsersService {
    private users = [];
    
    getUsers() {
        return this.users;
    }
    
    getUser(id: number) {
        return this.users.find(u => u.id === id);
    }
    
    createUser(data: CreateUserDto) {
        const user = { id: Date.now(), ...data };
        this.users.push(user);
        return user;
    }
}

// users.controller.ts
@Controller('users')
export class UsersController {
    constructor(private usersService: UsersService) {}
    
    @Get()
    getAll() {
        return this.usersService.getUsers();
    }
    
    @Get(':id')
    getOne(@Param('id') id: string) {
        return this.usersService.getUser(parseInt(id));
    }
    
    @Post()
    create(@Body() data: CreateUserDto) {
        return this.usersService.createUser(data);
    }
}
```

---

## Quick Reference Tables

### HTML Input Types
| Type | Validation | Example |
|------|------------|---------|
| text | None | Name field |
| email | Email format | Email field |
| password | Hidden input | Password field |
| number | Numeric only | Age field |
| tel | None (keyboard hint) | Phone field |
| url | URL format | Website field |
| date | Date picker | Birth date |
| time | Time picker | Appointment time |
| range | Slider | Volume control |
| color | Color picker | Theme color |
| file | File browser | Upload photo |
| checkbox | Boolean | Terms agreement |
| radio | Single selection | Gender |

### CSS Display Values
| Value | Flow | Width | Height |
|-------|------|-------|--------|
| block | New line | Full available | Set by content/style |
| inline | Same line | Content only | Content only |
| inline-block | Same line | Can set | Can set |
| flex | Flexbox | Full available | Set by content |
| grid | Grid | Full available | Set by content |
| none | Hidden | - | - |

### React Hooks Summary
| Hook | Purpose |
|------|---------|
| useState | Local state |
| useEffect | Side effects |
| useContext | Access context |
| useReducer | Complex state |
| useRef | Mutable reference |
| useMemo | Cache values |
| useCallback | Cache functions |

### HTTP Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

**Good luck on your exam! 🍀**

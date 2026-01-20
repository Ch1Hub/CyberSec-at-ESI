# 📝 Web & Mobile Development - Practice Exercises

**Total Exercises: 50+**  
**Difficulty Levels:** 🟢 Easy | 🟡 Medium | 🔴 Hard

---

## 📖 Table of Contents
1. [HTML5 Exercises](#-html5-exercises)
2. [CSS3 Exercises](#-css3-exercises)
3. [JavaScript Exercises](#-javascript-exercises)
4. [React Exercises](#-react-exercises)
5. [Flutter Exercises](#-flutter-exercises)
6. [Node.js & NestJS Exercises](#-nodejs--nestjs-exercises)

---

# 🌐 HTML5 Exercises

## Exercise 1: Basic Form 🟢
Complete the registration form:

```html
<!-- Complete the blanks -->
<form ______="POST" ______="/api/register">
    <label ______="username">Username:</label>
    <input ______="text" ______="username" ______="username" ______>
    
    <label for="email">Email:</label>
    <input ______="______" name="email" id="email" required>
    
    <label for="password">Password:</label>
    <input type="______" name="password" ______="6">
    
    <______ type="submit">Register</______>
</form>
```

<details>
<summary>✅ Solution</summary>

```html
<form method="POST" action="/api/register">
    <label for="username">Username:</label>
    <input type="text" name="username" id="username" required>
    
    <label for="email">Email:</label>
    <input type="email" name="email" id="email" required>
    
    <label for="password">Password:</label>
    <input type="password" name="password" minlength="6">
    
    <button type="submit">Register</button>
</form>
```
</details>

---

## Exercise 2: Form Validation 🟢
Add validation attributes:

```html
<!-- Add: required, pattern (only letters), placeholder, maxlength of 50 -->
<input type="text" name="fullname" ______ ______="[______]+" ______="Enter your full name" ______="50">

<!-- Add: required, min value 18, max value 120 -->
<input type="number" name="age" ______ ______="18" ______="120">

<!-- Add: required, pattern for phone (digits only, 10 chars) -->
<input type="tel" name="phone" ______ ______="[0-9]{10}" ______="0612345678">
```

<details>
<summary>✅ Solution</summary>

```html
<input type="text" name="fullname" required pattern="[a-zA-Z\s]+" placeholder="Enter your full name" maxlength="50">

<input type="number" name="age" required min="18" max="120">

<input type="tel" name="phone" required pattern="[0-9]{10}" placeholder="0612345678">
```
</details>

---

## Exercise 3: Complete Table 🟢
Complete the HTML table structure:

```html
<______>
    <______>Student Grades</______>
    <______>
        <tr>
            <______>Name</______>
            <th>Grade</th>
        </tr>
    </______>
    <______>
        <______>
            <td>Ali</td>
            <______>18</______>
        </______>
        <tr>
            <td>Sara</td>
            <td>16</td>
        </tr>
    </______>
    <______>
        <tr>
            <td ______="2">Average: 17</td>
        </tr>
    </______>
</table>
```

<details>
<summary>✅ Solution</summary>

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
        <tr>
            <td>Sara</td>
            <td>16</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="2">Average: 17</td>
        </tr>
    </tfoot>
</table>
```
</details>

---

## Exercise 4: Dropdown with Groups 🟡
Create a dropdown with option groups:

```html
<______>
    <______ ______="Frontend">
        <______ ______="html">HTML</______>
        <option value="css">CSS</option>
        <option value="js">JavaScript</option>
    </______>
    <optgroup ______="Backend">
        <option value="node">Node.js</option>
        <option value="python">Python</option>
    </optgroup>
</______>
```

<details>
<summary>✅ Solution</summary>

```html
<select>
    <optgroup label="Frontend">
        <option value="html">HTML</option>
        <option value="css">CSS</option>
        <option value="js">JavaScript</option>
    </optgroup>
    <optgroup label="Backend">
        <option value="node">Node.js</option>
        <option value="python">Python</option>
    </optgroup>
</select>
```
</details>

---

## Exercise 5: Geolocation API 🟡
Complete the geolocation code:

```javascript
// Get user's current location
navigator.______.______(
    function(______) {
        var lat = position.______.______;
        var lng = position.coords.______;
        console.log("Latitude: " + lat);
        console.log("Longitude: " + lng);
    },
    function(______) {
        console.log("Error: " + error.______);
    }
);
```

<details>
<summary>✅ Solution</summary>

```javascript
navigator.geolocation.getCurrentPosition(
    function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        console.log("Latitude: " + lat);
        console.log("Longitude: " + lng);
    },
    function(error) {
        console.log("Error: " + error.message);
    }
);
```
</details>

---

## Exercise 6: Drag and Drop 🟡
Complete the drag and drop functionality:

```html
<img id="img1" src="photo.jpg" ______="true" ______="drag(event)">
<div id="dropzone" ______="drop(event)" ______="allowDrop(event)"></div>

<script>
function drag(ev) {
    ev.______.______("text", ev.______.id);
}

function allowDrop(ev) {
    ev.______();
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.______("text");
    ev.target.______(document.______(data));
}
</script>
```

<details>
<summary>✅ Solution</summary>

```html
<img id="img1" src="photo.jpg" draggable="true" ondragstart="drag(event)">
<div id="dropzone" ondrop="drop(event)" ondragover="allowDrop(event)"></div>

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
</details>

---

## Exercise 7: WebSocket 🟡
Complete the WebSocket connection:

```javascript
// Create WebSocket connection
const socket = new ______("wss://example.com/socket");

// Connection opened
socket.______ = () => {
    console.log("Connected to server");
    socket.______("Hello, server!");
};

// Message received
socket.______ = (event) => {
    console.log("Received:", event.______);
};

// Error handling
socket.______ = (error) => {
    console.log("Error:", error);
};

// Connection closed
socket.______ = () => {
    console.log("Disconnected");
};
```

<details>
<summary>✅ Solution</summary>

```javascript
const socket = new WebSocket("wss://example.com/socket");

socket.onopen = () => {
    console.log("Connected to server");
    socket.send("Hello, server!");
};

socket.onmessage = (event) => {
    console.log("Received:", event.data);
};

socket.onerror = (error) => {
    console.log("Error:", error);
};

socket.onclose = () => {
    console.log("Disconnected");
};
```
</details>

---

## Exercise 8: Canvas Drawing 🔴
Draw shapes on canvas:

```javascript
var canvas = document.______("myCanvas");
var ctx = canvas.______("2d");

// Draw a blue filled rectangle at (10, 10) with size 100x50
ctx.______ = "blue";
ctx.______(10, 10, 100, 50);

// Draw a red circle at center (200, 100) with radius 40
ctx.______();
ctx.fillStyle = "red";
ctx.______(200, 100, 40, 0, 2 * Math.PI);
ctx.______();

// Draw a line from (0, 0) to (300, 150)
ctx.beginPath();
ctx.______(0, 0);
ctx.______(300, 150);
ctx.______();
```

<details>
<summary>✅ Solution</summary>

```javascript
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// Draw a blue filled rectangle
ctx.fillStyle = "blue";
ctx.fillRect(10, 10, 100, 50);

// Draw a red circle
ctx.beginPath();
ctx.fillStyle = "red";
ctx.arc(200, 100, 40, 0, 2 * Math.PI);
ctx.fill();

// Draw a line
ctx.beginPath();
ctx.moveTo(0, 0);
ctx.lineTo(300, 150);
ctx.stroke();
```
</details>

---

# 🎨 CSS3 Exercises

## Exercise 9: Selectors 🟢
Complete the CSS selectors:

```css
/* Select all paragraphs */
______ { color: blue; }

/* Select element with class "highlight" */
______ { background: yellow; }

/* Select element with id "header" */
______ { font-size: 24px; }

/* Select links inside divs */
______ ______ { text-decoration: none; }

/* Select direct children paragraphs of article */
article ______ p { margin: 10px; }
```

<details>
<summary>✅ Solution</summary>

```css
p { color: blue; }
.highlight { background: yellow; }
#header { font-size: 24px; }
div a { text-decoration: none; }
article > p { margin: 10px; }
```
</details>

---

## Exercise 10: Position Property 🟢
Complete the positioning:

```css
/* Fixed navbar at top */
.navbar {
    ______: fixed;
    ______: 0;
    ______: 0;
    ______: 100%;
    z-index: 1000;
}

/* Centered modal */
.modal {
    position: ______;
    top: ______;
    left: 50%;
    ______: translate(-50%, -50%);
}

/* Sticky sidebar */
.sidebar {
    position: ______;
    ______: 20px;
}
```

<details>
<summary>✅ Solution</summary>

```css
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
}

.modal {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.sidebar {
    position: sticky;
    top: 20px;
}
```
</details>

---

## Exercise 11: Flexbox Container 🟢
Complete the flexbox layout:

```css
/* Centered content */
.centered {
    ______: flex;
    ______: center;
    ______: center;
    height: 100vh;
}

/* Navigation with space between */
.nav {
    display: ______;
    justify-______: space-between;
    align-______: center;
}

/* Wrapping cards */
.card-container {
    display: flex;
    ______: wrap;
    ______: 20px;
}
```

<details>
<summary>✅ Solution</summary>

```css
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
```
</details>

---

## Exercise 12: Flexbox Items 🟡
Complete the flex item properties:

```css
/* Equal width columns */
.column {
    ______: 1;
}

/* Column that doesn't shrink */
.sidebar {
    flex-______: 0;
    flex-______: 250px;
}

/* Change item order */
.first-on-mobile {
    ______: -1;
}

/* Item-specific alignment */
.align-end {
    align-______: flex-end;
}
```

<details>
<summary>✅ Solution</summary>

```css
.column {
    flex: 1;
    /* or flex-grow: 1; */
}

.sidebar {
    flex-shrink: 0;
    flex-basis: 250px;
}

.first-on-mobile {
    order: -1;
}

.align-end {
    align-self: flex-end;
}
```
</details>

---

## Exercise 13: Media Queries 🟢
Complete the responsive styles:

```css
/* Mobile first - base styles */
.container {
    width: 100%;
    padding: 10px;
}

/* Tablet (768px and up) */
@______ ______ and (______: 768px) {
    .container {
        width: 750px;
        margin: 0 auto;
    }
}

/* Desktop (1024px and up) */
@media ______ and (min-______: 1024px) {
    .container {
        ______: 960px;
    }
}

/* Range: between 400px and 700px */
@media screen and (min-width: 400px) ______ (______: 700px) {
    body {
        background: lightblue;
    }
}
```

<details>
<summary>✅ Solution</summary>

```css
.container {
    width: 100%;
    padding: 10px;
}

@media screen and (min-width: 768px) {
    .container {
        width: 750px;
        margin: 0 auto;
    }
}

@media screen and (min-width: 1024px) {
    .container {
        width: 960px;
    }
}

@media screen and (min-width: 400px) and (max-width: 700px) {
    body {
        background: lightblue;
    }
}
```
</details>

---

## Exercise 14: Dark Mode 🟡
Create dark mode styles:

```css
/* Default light theme */
body {
    background-color: white;
    color: #333;
}

/* Dark mode preference */
@media (______-______-______: ______) {
    body {
        ______: #1a1a1a;
        ______: #f0f0f0;
    }
    
    a {
        color: #6db3f2;
    }
}
```

<details>
<summary>✅ Solution</summary>

```css
body {
    background-color: white;
    color: #333;
}

@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: #f0f0f0;
    }
    
    a {
        color: #6db3f2;
    }
}
```
</details>

---

## Exercise 15: Print Styles 🟡
Create print-specific styles:

```css
@media ______ {
    /* Hide navigation and buttons */
    nav, .no-print, button {
        ______: none;
    }
    
    /* Black text on white */
    body {
        ______: black;
        ______: white;
    }
    
    /* Show link URLs */
    a[href]::______ {
        ______: " (" attr(href) ")";
    }
    
    /* Page breaks */
    h1 {
        page-______-before: always;
    }
}
```

<details>
<summary>✅ Solution</summary>

```css
@media print {
    nav, .no-print, button {
        display: none;
    }
    
    body {
        color: black;
        background: white;
    }
    
    a[href]::after {
        content: " (" attr(href) ")";
    }
    
    h1 {
        page-break-before: always;
    }
}
```
</details>

---

## Exercise 16: Complete Card Layout 🔴
Create a responsive card grid:

```css
.cards {
    ______: flex;
    ______: wrap;
    ______: 20px;
    ______: center;
}

.card {
    ______: 1 1 300px;  /* grow, shrink, basis */
    max-______: 400px;
    padding: 20px;
    border-______: 8px;
    box-______: 0 2px 8px rgba(0,0,0,0.1);
}

@media (______: 600px) {
    .card {
        flex-basis: ______;
    }
}
```

<details>
<summary>✅ Solution</summary>

```css
.cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}

.card {
    flex: 1 1 300px;
    max-width: 400px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

@media (max-width: 600px) {
    .card {
        flex-basis: 100%;
    }
}
```
</details>

---

# 💻 JavaScript Exercises

## Exercise 17: Array Methods - map 🟢
Transform arrays using map:

```javascript
const numbers = [1, 2, 3, 4, 5];

// Double each number
const doubled = numbers.______(n => n ______ 2);
// Result: [2, 4, 6, 8, 10]

const users = [
    { name: "Ali", age: 25 },
    { name: "Sara", age: 22 }
];

// Get only names
const names = users.______(user => user.______);
// Result: ["Ali", "Sara"]
```

<details>
<summary>✅ Solution</summary>

```javascript
const doubled = numbers.map(n => n * 2);
const names = users.map(user => user.name);
```
</details>

---

## Exercise 18: Array Methods - filter 🟢
Filter arrays:

```javascript
const products = [
    { name: "Laptop", price: 1000, inStock: true },
    { name: "Phone", price: 500, inStock: false },
    { name: "Tablet", price: 300, inStock: true },
    { name: "Watch", price: 200, inStock: true }
];

// Get products in stock
const available = products.______(p => p.______);

// Get products under $400
const cheap = products.______(p => p.______ ______ 400);

// Get expensive products (price >= 500) that are in stock
const expensiveAvailable = products.filter(p => p.______ >= 500 ______ p.______);
```

<details>
<summary>✅ Solution</summary>

```javascript
const available = products.filter(p => p.inStock);
const cheap = products.filter(p => p.price < 400);
const expensiveAvailable = products.filter(p => p.price >= 500 && p.inStock);
```
</details>

---

## Exercise 19: Array Methods - reduce 🟡
Reduce arrays to single values:

```javascript
const numbers = [1, 2, 3, 4, 5];

// Sum all numbers
const sum = numbers.______((acc, n) => acc ______ n, ______);
// Result: 15

// Find maximum
const max = numbers.reduce((______, n) => n > max ? ______ : max, numbers[0]);
// Result: 5

const cart = [
    { item: "Book", price: 20, qty: 2 },
    { item: "Pen", price: 5, qty: 10 }
];

// Calculate total cost
const total = cart.______(
    (sum, item) => sum + (item.______ * item.______), 
    0
);
// Result: 90
```

<details>
<summary>✅ Solution</summary>

```javascript
const sum = numbers.reduce((acc, n) => acc + n, 0);
const max = numbers.reduce((max, n) => n > max ? n : max, numbers[0]);
const total = cart.reduce(
    (sum, item) => sum + (item.price * item.qty), 
    0
);
```
</details>

---

## Exercise 20: Destructuring 🟡
Complete the destructuring:

```javascript
const user = { 
    name: "Ali", 
    age: 25, 
    address: { city: "Algiers", country: "Algeria" }
};

// Object destructuring
const { ______, ______ } = user;
console.log(name); // "Ali"
console.log(age);  // 25

// Nested destructuring
const { address: { ______, ______ } } = user;
console.log(city);    // "Algiers"
console.log(country); // "Algeria"

// Array destructuring
const colors = ["red", "green", "blue", "yellow"];
const [first, ______, ...______] = colors;
console.log(first);  // "red"
console.log(second); // "green"
console.log(rest);   // ["blue", "yellow"]
```

<details>
<summary>✅ Solution</summary>

```javascript
const { name, age } = user;
const { address: { city, country } } = user;
const [first, second, ...rest] = colors;
```
</details>

---

## Exercise 21: Spread Operator 🟡
Use spread operator:

```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// Combine arrays
const combined = [______arr1, ______arr2];
// Result: [1, 2, 3, 4, 5, 6]

// Add element at beginning
const withZero = [0, ______arr1];
// Result: [0, 1, 2, 3]

const obj1 = { a: 1, b: 2 };
const obj2 = { c: 3, d: 4 };

// Merge objects
const merged = { ______obj1, ______obj2 };
// Result: { a: 1, b: 2, c: 3, d: 4 }

// Clone and modify
const updated = { ______obj1, b: 10 };
// Result: { a: 1, b: 10 }
```

<details>
<summary>✅ Solution</summary>

```javascript
const combined = [...arr1, ...arr2];
const withZero = [0, ...arr1];
const merged = { ...obj1, ...obj2 };
const updated = { ...obj1, b: 10 };
```
</details>

---

## Exercise 22: DOM Selection 🟢
Select DOM elements:

```javascript
// Get element by ID
const header = document.______("header");

// Get first element matching selector
const firstButton = document.______("button.primary");

// Get all elements matching selector
const allLinks = document.______("a.nav-link");

// Get elements by class name
const cards = document.______("card");

// Get elements by tag name
const paragraphs = document.______("p");
```

<details>
<summary>✅ Solution</summary>

```javascript
const header = document.getElementById("header");
const firstButton = document.querySelector("button.primary");
const allLinks = document.querySelectorAll("a.nav-link");
const cards = document.getElementsByClassName("card");
const paragraphs = document.getElementsByTagName("p");
```
</details>

---

## Exercise 23: DOM Manipulation 🟡
Modify DOM elements:

```javascript
const element = document.getElementById("myDiv");

// Change text content
element.______ = "New text";

// Change HTML content
element.______ = "<strong>Bold text</strong>";

// Add a class
element.______.______("active");

// Remove a class
element.classList.______("hidden");

// Toggle a class
element.classList.______("visible");

// Set attribute
element.______("data-id", "123");

// Change style
element.______.backgroundColor = "blue";
element.style.______ = "20px";
```

<details>
<summary>✅ Solution</summary>

```javascript
element.textContent = "New text";
element.innerHTML = "<strong>Bold text</strong>";
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("visible");
element.setAttribute("data-id", "123");
element.style.backgroundColor = "blue";
element.style.padding = "20px";
```
</details>

---

## Exercise 24: Event Handling 🟡
Handle DOM events:

```javascript
const button = document.getElementById("myButton");
const input = document.getElementById("myInput");
const form = document.getElementById("myForm");

// Click event
button.______("______", function(e) {
    console.log("Button clicked!");
});

// Input change event
input.addEventListener("______", function(e) {
    console.log("Value:", e.______.______);
});

// Form submit with prevention
form.addEventListener("submit", function(e) {
    e.______();  // Prevent page reload
    console.log("Form submitted!");
});

// Keyboard event
document.addEventListener("______", function(e) {
    console.log("Key pressed:", e.______);
});
```

<details>
<summary>✅ Solution</summary>

```javascript
button.addEventListener("click", function(e) {
    console.log("Button clicked!");
});

input.addEventListener("input", function(e) {
    console.log("Value:", e.target.value);
});

form.addEventListener("submit", function(e) {
    e.preventDefault();
    console.log("Form submitted!");
});

document.addEventListener("keydown", function(e) {
    console.log("Key pressed:", e.key);
});
```
</details>

---

## Exercise 25: Promises & Fetch 🔴
Work with async operations:

```javascript
// Fetch data from API
______("/api/users")
    .______(response => response.______())
    .______(data => {
        console.log("Users:", data);
    })
    .______(error => {
        console.log("Error:", error);
    });

// Async/await version
______ function getUsers() {
    ______ {
        const response = ______ fetch("/api/users");
        const data = ______ response.json();
        console.log("Users:", data);
    } ______ (error) {
        console.log("Error:", error);
    }
}
```

<details>
<summary>✅ Solution</summary>

```javascript
fetch("/api/users")
    .then(response => response.json())
    .then(data => {
        console.log("Users:", data);
    })
    .catch(error => {
        console.log("Error:", error);
    });

async function getUsers() {
    try {
        const response = await fetch("/api/users");
        const data = await response.json();
        console.log("Users:", data);
    } catch (error) {
        console.log("Error:", error);
    }
}
```
</details>

---

# ⚛️ React Exercises

## Exercise 26: JSX Basics 🟢
Complete the JSX:

```jsx
function Welcome() {
    const name = "Mohamed";
    const isLoggedIn = true;
    
    return (
        <______>
            <h1>Hello, {______}!</h1>
            
            {/* Show only if logged in */}
            {______ ______ <p>Welcome back!</p>}
            
            {/* Conditional rendering */}
            {isLoggedIn ______ <LogoutBtn /> ______ <LoginBtn />}
        </______>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
function Welcome() {
    const name = "Mohamed";
    const isLoggedIn = true;
    
    return (
        <div>
            <h1>Hello, {name}!</h1>
            {isLoggedIn && <p>Welcome back!</p>}
            {isLoggedIn ? <LogoutBtn /> : <LoginBtn />}
        </div>
    );
}
```
</details>

---

## Exercise 27: Functional Component with Props 🟢
Create a component with props:

```jsx
// UserCard component
function UserCard(______) {
    return (
        <div className="card">
            <h2>{______.name}</h2>
            <p>Email: {props.______}</p>
            <p>Age: {props.______}</p>
        </div>
    );
}

// Using the component
function App() {
    return (
        <div>
            <______ 
                ______="Ali" 
                ______="ali@email.com" 
                ______={25} 
            />
        </div>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
function UserCard(props) {
    return (
        <div className="card">
            <h2>{props.name}</h2>
            <p>Email: {props.email}</p>
            <p>Age: {props.age}</p>
        </div>
    );
}

function App() {
    return (
        <div>
            <UserCard 
                name="Ali" 
                email="ali@email.com" 
                age={25} 
            />
        </div>
    );
}
```
</details>

---

## Exercise 28: Props Destructuring 🟢
Use destructuring with props:

```jsx
// Before: function Greeting(props)
function Greeting({ ______, ______ }) {
    return (
        <div>
            <h1>Hello, {______}!</h1>
            <p>You are {______} years old.</p>
        </div>
    );
}

// With default values
function Button({ ______ = "Click me", ______ = "blue" }) {
    return (
        <button style={{ backgroundColor: color }}>
            {______}
        </button>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
function Greeting({ name, age }) {
    return (
        <div>
            <h1>Hello, {name}!</h1>
            <p>You are {age} years old.</p>
        </div>
    );
}

function Button({ text = "Click me", color = "blue" }) {
    return (
        <button style={{ backgroundColor: color }}>
            {text}
        </button>
    );
}
```
</details>

---

## Exercise 29: useState Hook 🟢
Implement state management:

```jsx
import { ______ } from 'react';

function Counter() {
    // Declare count state with initial value 0
    const [______, ______] = ______(0);
    
    return (
        <div>
            <p>Count: {______}</p>
            <button ______={() => ______(count + 1)}>+1</button>
            <button onClick={() => ______(______ => prev - 1)}>-1</button>
            <button onClick={() => setCount(______)}>Reset</button>
        </div>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(prev => prev - 1)}>-1</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}
```
</details>

---

## Exercise 30: useState with Objects 🟡
Manage object state:

```jsx
import { useState } from 'react';

function UserForm() {
    const [user, setUser] = useState({
        name: '',
        email: '',
        age: 0
    });
    
    const handleChange = (e) => {
        const { ______, ______ } = e.target;
        setUser({
            ______user,  // Keep existing fields
            [name]: ______  // Update changed field
        });
    };
    
    return (
        <form>
            <input 
                ______="name" 
                ______={user.name} 
                ______={handleChange} 
            />
            <input 
                name="email" 
                value={______.______} 
                onChange={______} 
            />
        </form>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
import { useState } from 'react';

function UserForm() {
    const [user, setUser] = useState({
        name: '',
        email: '',
        age: 0
    });
    
    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser({
            ...user,
            [name]: value
        });
    };
    
    return (
        <form>
            <input 
                name="name" 
                value={user.name} 
                onChange={handleChange} 
            />
            <input 
                name="email" 
                value={user.email} 
                onChange={handleChange} 
            />
        </form>
    );
}
```
</details>

---

## Exercise 31: useState with Arrays 🟡
Manage array state:

```jsx
import { useState } from 'react';

function TodoList() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    
    const addTodo = () => {
        // Add new todo to array
        setTodos([______todos, ______]);
        setInput('');
    };
    
    const removeTodo = (index) => {
        // Remove todo at index
        setTodos(todos.______((___, i) => i ______ index));
    };
    
    return (
        <div>
            <input 
                value={input} 
                onChange={(e) => ______(e.target.______)} 
            />
            <button onClick={______}>Add</button>
            
            <ul>
                {todos.______(
                    (todo, index) => (
                        <li ______={index}>
                            {todo}
                            <button onClick={() => ______(index)}>X</button>
                        </li>
                    )
                )}
            </ul>
        </div>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
import { useState } from 'react';

function TodoList() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    
    const addTodo = () => {
        setTodos([...todos, input]);
        setInput('');
    };
    
    const removeTodo = (index) => {
        setTodos(todos.filter((_, i) => i !== index));
    };
    
    return (
        <div>
            <input 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
            />
            <button onClick={addTodo}>Add</button>
            
            <ul>
                {todos.map(
                    (todo, index) => (
                        <li key={index}>
                            {todo}
                            <button onClick={() => removeTodo(index)}>X</button>
                        </li>
                    )
                )}
            </ul>
        </div>
    );
}
```
</details>

---

## Exercise 32: useEffect Hook 🟡
Implement side effects:

```jsx
import { useState, ______ } from 'react';

function DataFetcher() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    
    // Run on mount only
    ______(() => {
        fetch('/api/data')
            .then(res => res.json())
            .then(result => {
                ______(result);
                ______(false);
            });
    }, [______]);  // Empty array = run once
    
    // Run when 'count' changes
    const [count, setCount] = useState(0);
    
    useEffect(() => {
        document.title = `Count: ${______}`;
    }, [______]);  // Dependency array
    
    // Cleanup on unmount
    useEffect(() => {
        const timer = setInterval(() => console.log("tick"), 1000);
        
        ______ () => {
            ______(timer);  // Cleanup function
        };
    }, []);
    
    if (loading) return <p>Loading...</p>;
    return <div>{data.name}</div>;
}
```

<details>
<summary>✅ Solution</summary>

```jsx
import { useState, useEffect } from 'react';

function DataFetcher() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetch('/api/data')
            .then(res => res.json())
            .then(result => {
                setData(result);
                setLoading(false);
            });
    }, []);
    
    const [count, setCount] = useState(0);
    
    useEffect(() => {
        document.title = `Count: ${count}`;
    }, [count]);
    
    useEffect(() => {
        const timer = setInterval(() => console.log("tick"), 1000);
        
        return () => {
            clearInterval(timer);
        };
    }, []);
    
    if (loading) return <p>Loading...</p>;
    return <div>{data.name}</div>;
}
```
</details>

---

## Exercise 33: Event Handling in React 🟢
Handle events:

```jsx
function EventDemo() {
    // Simple click handler
    function handleClick() {
        alert("Clicked!");
    }
    
    // Click with parameter
    function greet(name) {
        alert(`Hello, ${name}!`);
    }
    
    // Form submit
    function handleSubmit(e) {
        e.______();  // Prevent page reload
        console.log("Submitted!");
    }
    
    return (
        <div>
            {/* Basic click */}
            <button ______={handleClick}>Click me</button>
            
            {/* Click with parameter */}
            <button onClick={______ => ______("Ali")}>Greet Ali</button>
            
            {/* Form submit */}
            <form ______={handleSubmit}>
                <button type="submit">Submit</button>
            </form>
            
            {/* Inline handler */}
            <button ______={() => ______.log("Inline!")}>Log</button>
        </div>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
function EventDemo() {
    function handleClick() {
        alert("Clicked!");
    }
    
    function greet(name) {
        alert(`Hello, ${name}!`);
    }
    
    function handleSubmit(e) {
        e.preventDefault();
        console.log("Submitted!");
    }
    
    return (
        <div>
            <button onClick={handleClick}>Click me</button>
            <button onClick={() => greet("Ali")}>Greet Ali</button>
            <form onSubmit={handleSubmit}>
                <button type="submit">Submit</button>
            </form>
            <button onClick={() => console.log("Inline!")}>Log</button>
        </div>
    );
}
```
</details>

---

## Exercise 34: Rendering Lists 🟢
Render lists with map:

```jsx
function UserList() {
    const users = [
        { id: 1, name: "Ali", role: "Admin" },
        { id: 2, name: "Sara", role: "User" },
        { id: 3, name: "Omar", role: "User" }
    ];
    
    return (
        <ul>
            {users.______(user => (
                <li ______={user.______}>
                    <strong>{user.______}</strong> - {user.role}
                </li>
            ))}
        </ul>
    );
}

// Rendering with condition
function FilteredList() {
    const items = [1, 2, 3, 4, 5, 6];
    
    return (
        <ul>
            {items
                .______(n => n % 2 === 0)  // Only even
                .map(n => <li key={n}>{n}</li>)
            }
        </ul>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
function UserList() {
    const users = [
        { id: 1, name: "Ali", role: "Admin" },
        { id: 2, name: "Sara", role: "User" },
        { id: 3, name: "Omar", role: "User" }
    ];
    
    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>
                    <strong>{user.name}</strong> - {user.role}
                </li>
            ))}
        </ul>
    );
}

function FilteredList() {
    const items = [1, 2, 3, 4, 5, 6];
    
    return (
        <ul>
            {items
                .filter(n => n % 2 === 0)
                .map(n => <li key={n}>{n}</li>)
            }
        </ul>
    );
}
```
</details>

---

## Exercise 35: Context API 🔴
Implement global state with Context:

```jsx
import { ______, useContext, useState } from 'react';

// 1. Create context
const ThemeContext = ______();

// 2. Provider component
function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    
    const toggleTheme = () => {
        setTheme(t => t === 'light' ? '______' : '______');
    };
    
    return (
        <ThemeContext.______ ______={{ theme, toggleTheme }}>
            {______}
        </ThemeContext.Provider>
    );
}

// 3. Use context in component
function Header() {
    const { ______, ______ } = ______(ThemeContext);
    
    return (
        <header className={theme}>
            <p>Current theme: {______}</p>
            <button ______={toggleTheme}>Toggle Theme</button>
        </header>
    );
}

// 4. App setup
function App() {
    return (
        <______>
            <Header />
            <Main />
        </ThemeProvider>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext();

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

function Header() {
    const { theme, toggleTheme } = useContext(ThemeContext);
    
    return (
        <header className={theme}>
            <p>Current theme: {theme}</p>
            <button onClick={toggleTheme}>Toggle Theme</button>
        </header>
    );
}

function App() {
    return (
        <ThemeProvider>
            <Header />
            <Main />
        </ThemeProvider>
    );
}
```
</details>

---

## Exercise 36: CSS Modules in React 🟡
Use CSS Modules:

```jsx
// Button.module.css
/*
.button {
    padding: 10px 20px;
    border-radius: 5px;
}
.primary {
    background: blue;
    color: white;
}
*/

// Button.jsx
import ______ from './Button.______.css';

function Button({ children, variant = "primary" }) {
    return (
        <button ______={`${styles.______} ${styles[______]}`}>
            {children}
        </button>
    );
}

// Usage
<Button ______="primary">Click me</Button>
```

<details>
<summary>✅ Solution</summary>

```jsx
import styles from './Button.module.css';

function Button({ children, variant = "primary" }) {
    return (
        <button className={`${styles.button} ${styles[variant]}`}>
            {children}
        </button>
    );
}

// Usage
<Button variant="primary">Click me</Button>
```
</details>

---

# 📱 Flutter Exercises

## Exercise 37: StatelessWidget 🟢
Create a stateless widget:

```dart
class ______ extends ______ {
    @______
    Widget ______(BuildContext context) {
        return Scaffold(
            appBar: ______( 
                title: Text("My App")
            ),
            body: ______(
                child: Text("Hello World"),
            ),
        );
    }
}
```

<details>
<summary>✅ Solution</summary>

```dart
class HomePage extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text("My App")
            ),
            body: Center(
                child: Text("Hello World"),
            ),
        );
    }
}
```
</details>

---

## Exercise 38: StatefulWidget 🟢
Create a counter with StatefulWidget:

```dart
class Counter extends ______ {
    @override
    ______<Counter> ______() => _CounterState();
}

class _CounterState extends ______<Counter> {
    int count = 0;
    
    void increment() {
        ______(() {
            ______++;
        });
    }
    
    @override
    Widget ______(BuildContext context) {
        return Column(
            children: [
                Text('Count: $______'),
                ElevatedButton(
                    ______: increment,
                    child: Text('Add'),
                ),
            ],
        );
    }
}
```

<details>
<summary>✅ Solution</summary>

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
</details>

---

## Exercise 39: Scaffold Structure 🟢
Complete the Scaffold:

```dart
Scaffold(
    ______: AppBar(
        ______: Text("My App"),
        ______: [
            IconButton(
                icon: Icon(Icons.search),
                ______: () {},
            ),
        ],
    ),
    ______: Center(
        child: Text("Hello"),
    ),
    ______: FloatingActionButton(
        onPressed: () {},
        child: Icon(Icons.______),
    ),
    ______: Drawer(
        child: ListView(),
    ),
)
```

<details>
<summary>✅ Solution</summary>

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
        child: ListView(),
    ),
)
```
</details>

---

## Exercise 40: TextField & TextFormField 🟡
Create input fields:

```dart
// Basic TextField
______(
    ______: InputDecoration(
        ______: "Enter name",
        ______: "Your name here",
        ______: OutlineInputBorder(),
        ______: Icon(Icons.person),
    ),
    ______: (value) => print(value),
)

// TextFormField with validation
______( 
    decoration: InputDecoration(labelText: "Email"),
    ______: (value) {
        if (value == null || value.______) {
            return "Email is ______";
        }
        if (!value.______('@')) {
            return "Invalid email";
        }
        return ______;
    },
)
```

<details>
<summary>✅ Solution</summary>

```dart
TextField(
    decoration: InputDecoration(
        labelText: "Enter name",
        hintText: "Your name here",
        border: OutlineInputBorder(),
        prefixIcon: Icon(Icons.person),
    ),
    onChanged: (value) => print(value),
)

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
```
</details>

---

## Exercise 41: Row & Column Layout 🟢
Create layouts:

```dart
// Horizontal layout
______(
    ______: MainAxisAlignment.spaceBetween,
    ______: CrossAxisAlignment.center,
    ______: [
        Text("Left"),
        Text("Center"),
        Text("Right"),
    ],
)

// Vertical layout
______(
    mainAxisAlignment: MainAxisAlignment.______,
    crossAxisAlignment: CrossAxisAlignment.______,
    children: [
        Text("Top"),
        Text("Middle"),
        Text("Bottom"),
    ],
)
```

<details>
<summary>✅ Solution</summary>

```dart
Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
        Text("Left"),
        Text("Center"),
        Text("Right"),
    ],
)

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
</details>

---

## Exercise 42: ListView 🟡
Create scrollable lists:

```dart
// Static list
______( 
    ______: [
        ListTile(title: Text("Item 1")),
        ListTile(title: Text("Item 2")),
        ListTile(title: Text("Item 3")),
    ],
)

// Dynamic list
final items = ["Apple", "Banana", "Cherry"];

ListView.______(
    ______: items.length,
    ______: (context, index) {
        return ListTile(
            ______: Text(items[______]),
            ______: Icon(Icons.chevron_right),
        );
    },
)
```

<details>
<summary>✅ Solution</summary>

```dart
ListView(
    children: [
        ListTile(title: Text("Item 1")),
        ListTile(title: Text("Item 2")),
        ListTile(title: Text("Item 3")),
    ],
)

ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, index) {
        return ListTile(
            title: Text(items[index]),
            trailing: Icon(Icons.chevron_right),
        );
    },
)
```
</details>

---

## Exercise 43: Navigation 🟡
Implement navigation:

```dart
// Navigate to new screen
Navigator.______(
    context,
    ______(______: (context) => SecondScreen()),
);

// Go back
Navigator.______(context);

// Named routes setup
MaterialApp(
    ______: '/',
    ______: {
        '/': (context) => HomeScreen(),
        '/details': (context) => DetailsScreen(),
    },
)

// Navigate using name
Navigator.______(context, '/details');
```

<details>
<summary>✅ Solution</summary>

```dart
Navigator.push(
    context,
    MaterialPageRoute(builder: (context) => SecondScreen()),
);

Navigator.pop(context);

MaterialApp(
    initialRoute: '/',
    routes: {
        '/': (context) => HomeScreen(),
        '/details': (context) => DetailsScreen(),
    },
)

Navigator.pushNamed(context, '/details');
```
</details>

---

## Exercise 44: Form Validation 🔴
Complete form validation:

```dart
class LoginForm extends StatefulWidget {
    @override
    State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
    final _formKey = ______<FormState>();
    
    void _submit() {
        if (_formKey.______!.______()) {
            print("Form is valid!");
        }
    }
    
    @override
    Widget build(BuildContext context) {
        return ______(
            ______: _formKey,
            child: Column(
                children: [
                    TextFormField(
                        decoration: InputDecoration(______: 'Email'),
                        ______: (value) {
                            if (value == null || value.isEmpty) {
                                return 'Email required';
                            }
                            return null;
                        },
                    ),
                    TextFormField(
                        decoration: InputDecoration(labelText: 'Password'),
                        ______: true,
                        validator: (value) {
                            if (value == null || value.______ < 6) {
                                return 'Min 6 characters';
                            }
                            return ______;
                        },
                    ),
                    ElevatedButton(
                        ______: _submit,
                        child: Text('Login'),
                    ),
                ],
            ),
        );
    }
}
```

<details>
<summary>✅ Solution</summary>

```dart
class _LoginFormState extends State<LoginForm> {
    final _formKey = GlobalKey<FormState>();
    
    void _submit() {
        if (_formKey.currentState!.validate()) {
            print("Form is valid!");
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
                                return 'Email required';
                            }
                            return null;
                        },
                    ),
                    TextFormField(
                        decoration: InputDecoration(labelText: 'Password'),
                        obscureText: true,
                        validator: (value) {
                            if (value == null || value.length < 6) {
                                return 'Min 6 characters';
                            }
                            return null;
                        },
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
</details>

---

## Exercise 45: Checkbox & Radio 🟡
Implement selection widgets:

```dart
// Checkbox
bool isChecked = false;

______(
    ______: isChecked,
    ______: (value) {
        ______(() {
            ______ = value!;
        });
    },
)

// Radio buttons
int selectedOption = 1;

______<int>(
    ______: 1,
    ______: selectedOption,
    ______: (value) {
        setState(() {
            ______ = value!;
        });
    },
)

Radio<int>(
    value: 2,
    groupValue: ______,
    onChanged: (value) {
        setState(() => selectedOption = value!);
    },
)
```

<details>
<summary>✅ Solution</summary>

```dart
Checkbox(
    value: isChecked,
    onChanged: (value) {
        setState(() {
            isChecked = value!;
        });
    },
)

Radio<int>(
    value: 1,
    groupValue: selectedOption,
    onChanged: (value) {
        setState(() {
            selectedOption = value!;
        });
    },
)

Radio<int>(
    value: 2,
    groupValue: selectedOption,
    onChanged: (value) {
        setState(() => selectedOption = value!);
    },
)
```
</details>

---

# 🖥️ Node.js & NestJS Exercises

## Exercise 46: HTTP Server 🟢
Create a basic HTTP server:

```javascript
var http = ______('http');
var port = 3000;

var server = http.______(function(______, ______) {
    // Set headers
    response.______(200, { 'Content-Type': 'text/html' });
    
    // Write response
    response.______("<h1>Hello World!</h1>");
    
    // End response
    response.______();
});

server.______(port);
console.log("Server running on port " + port);
```

<details>
<summary>✅ Solution</summary>

```javascript
var http = require('http');
var port = 3000;

var server = http.createServer(function(request, response) {
    response.writeHead(200, { 'Content-Type': 'text/html' });
    response.write("<h1>Hello World!</h1>");
    response.end();
});

server.listen(port);
console.log("Server running on port " + port);
```
</details>

---

## Exercise 47: Events System 🟢
Work with events:

```javascript
var events = ______('events');

// Create EventEmitter
var emitter = new events.______();

// Add listener
emitter.______(______, function(user) {
    console.log('User connected:', user.name);
});

// Add one-time listener
emitter.______('firstConnection', function() {
    console.log('First connection!');
});

// Emit events
emitter.______('userConnected', { name: 'Ali' });
emitter.emit('firstConnection');
emitter.emit('firstConnection');  // Won't run again
```

<details>
<summary>✅ Solution</summary>

```javascript
var events = require('events');

var emitter = new events.EventEmitter();

emitter.addListener('userConnected', function(user) {
    console.log('User connected:', user.name);
});

emitter.once('firstConnection', function() {
    console.log('First connection!');
});

emitter.emit('userConnected', { name: 'Ali' });
emitter.emit('firstConnection');
emitter.emit('firstConnection');
```
</details>

---

## Exercise 48: NestJS Module 🟡
Create a NestJS module:

```typescript
import { ______ } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@______({
    ______: [UsersController],
    ______: [UsersService],
    ______: [UsersService],
})
export class UsersModule {}
```

<details>
<summary>✅ Solution</summary>

```typescript
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
    controllers: [UsersController],
    providers: [UsersService],
    exports: [UsersService],
})
export class UsersModule {}
```
</details>

---

## Exercise 49: NestJS Controller 🟡
Create a REST controller:

```typescript
import { Controller, ______, ______, ______, ______, Param, Body } from '@nestjs/common';

@______('products')
export class ProductsController {
    constructor(private productsService: ProductsService) {}
    
    // GET /products
    @______()
    findAll() {
        return this.productsService.findAll();
    }
    
    // GET /products/:id
    @Get('______')
    findOne(@______('id') id: string) {
        return this.productsService.findOne(id);
    }
    
    // POST /products
    @______()
    create(@______() data: CreateProductDto) {
        return this.productsService.create(data);
    }
    
    // PUT /products/:id
    @______(':id')
    update(@Param('id') id: string, @Body() data: UpdateProductDto) {
        return this.productsService.update(id, data);
    }
    
    // DELETE /products/:id
    @______(':id')
    remove(@Param('id') id: string) {
        return this.productsService.remove(id);
    }
}
```

<details>
<summary>✅ Solution</summary>

```typescript
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';

@Controller('products')
export class ProductsController {
    constructor(private productsService: ProductsService) {}
    
    @Get()
    findAll() {
        return this.productsService.findAll();
    }
    
    @Get(':id')
    findOne(@Param('id') id: string) {
        return this.productsService.findOne(id);
    }
    
    @Post()
    create(@Body() data: CreateProductDto) {
        return this.productsService.create(data);
    }
    
    @Put(':id')
    update(@Param('id') id: string, @Body() data: UpdateProductDto) {
        return this.productsService.update(id, data);
    }
    
    @Delete(':id')
    remove(@Param('id') id: string) {
        return this.productsService.remove(id);
    }
}
```
</details>

---

## Exercise 50: NestJS Service 🟡
Create a service with dependency injection:

```typescript
import { ______ } from '@nestjs/common';

@______()
export class UsersService {
    private users = [
        { id: 1, name: 'Ali' },
        { id: 2, name: 'Sara' },
    ];
    
    ______() {
        return this.users;
    }
    
    ______(id: string) {
        return this.users.______(u => u.id === parseInt(id));
    }
    
    ______(data: CreateUserDto) {
        const newUser = { id: Date.now(), ...data };
        this.users.______(newUser);
        return newUser;
    }
    
    update(id: string, data: UpdateUserDto) {
        const index = this.users.______(u => u.id === parseInt(id));
        this.users[index] = { ...this.users[index], ...data };
        return this.users[index];
    }
    
    ______(id: string) {
        const index = this.users.findIndex(u => u.id === parseInt(id));
        return this.users.______(index, 1);
    }
}
```

<details>
<summary>✅ Solution</summary>

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
    
    create(data: CreateUserDto) {
        const newUser = { id: Date.now(), ...data };
        this.users.push(newUser);
        return newUser;
    }
    
    update(id: string, data: UpdateUserDto) {
        const index = this.users.findIndex(u => u.id === parseInt(id));
        this.users[index] = { ...this.users[index], ...data };
        return this.users[index];
    }
    
    remove(id: string) {
        const index = this.users.findIndex(u => u.id === parseInt(id));
        return this.users.splice(index, 1);
    }
}
```
</details>

---

# 🎯 Bonus: Complete Projects

## Project 1: React Todo App 🔴
Build a complete todo app:

```jsx
import { useState } from 'react';

function TodoApp() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    
    const addTodo = () => {
        if (input.trim()) {
            setTodos([...todos, { 
                id: Date.now(), 
                text: input, 
                completed: false 
            }]);
            setInput('');
        }
    };
    
    const toggleTodo = (id) => {
        // Complete this function
    };
    
    const deleteTodo = (id) => {
        // Complete this function
    };
    
    return (
        <div>
            <h1>Todo App</h1>
            {/* Complete the JSX */}
        </div>
    );
}
```

<details>
<summary>✅ Solution</summary>

```jsx
import { useState } from 'react';

function TodoApp() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    
    const addTodo = () => {
        if (input.trim()) {
            setTodos([...todos, { 
                id: Date.now(), 
                text: input, 
                completed: false 
            }]);
            setInput('');
        }
    };
    
    const toggleTodo = (id) => {
        setTodos(todos.map(todo => 
            todo.id === id 
                ? { ...todo, completed: !todo.completed }
                : todo
        ));
    };
    
    const deleteTodo = (id) => {
        setTodos(todos.filter(todo => todo.id !== id));
    };
    
    return (
        <div>
            <h1>Todo App</h1>
            <input 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addTodo()}
                placeholder="Add todo..."
            />
            <button onClick={addTodo}>Add</button>
            
            <ul>
                {todos.map(todo => (
                    <li key={todo.id}>
                        <span 
                            style={{ 
                                textDecoration: todo.completed ? 'line-through' : 'none',
                                cursor: 'pointer'
                            }}
                            onClick={() => toggleTodo(todo.id)}
                        >
                            {todo.text}
                        </span>
                        <button onClick={() => deleteTodo(todo.id)}>Delete</button>
                    </li>
                ))}
            </ul>
            
            <p>
                {todos.filter(t => !t.completed).length} items left
            </p>
        </div>
    );
}

export default TodoApp;
```
</details>

---

## Project 2: Flutter Counter with Theme 🔴
Build a themed counter app:

```dart
// Complete this Flutter app with:
// 1. Counter with increment/decrement
// 2. Theme toggle (light/dark)
// 3. Reset button

class CounterApp extends StatefulWidget {
    @override
    State<CounterApp> createState() => _CounterAppState();
}

class _CounterAppState extends State<CounterApp> {
    int count = 0;
    bool isDark = false;
    
    // Complete the implementation
}
```

<details>
<summary>✅ Solution</summary>

```dart
class CounterApp extends StatefulWidget {
    @override
    State<CounterApp> createState() => _CounterAppState();
}

class _CounterAppState extends State<CounterApp> {
    int count = 0;
    bool isDark = false;
    
    void increment() => setState(() => count++);
    void decrement() => setState(() => count--);
    void reset() => setState(() => count = 0);
    void toggleTheme() => setState(() => isDark = !isDark);
    
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            theme: isDark ? ThemeData.dark() : ThemeData.light(),
            home: Scaffold(
                appBar: AppBar(
                    title: Text("Counter App"),
                    actions: [
                        IconButton(
                            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
                            onPressed: toggleTheme,
                        ),
                    ],
                ),
                body: Center(
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                            Text(
                                'Count: $count',
                                style: TextStyle(fontSize: 48),
                            ),
                            SizedBox(height: 20),
                            Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                    ElevatedButton(
                                        onPressed: decrement,
                                        child: Icon(Icons.remove),
                                    ),
                                    SizedBox(width: 20),
                                    ElevatedButton(
                                        onPressed: reset,
                                        child: Text("Reset"),
                                    ),
                                    SizedBox(width: 20),
                                    ElevatedButton(
                                        onPressed: increment,
                                        child: Icon(Icons.add),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ),
        );
    }
}
```
</details>

---

## Project 3: NestJS REST API 🔴
Build a complete REST API:

```typescript
// Complete a CRUD API for a "tasks" resource
// Endpoints:
// GET /tasks - list all tasks
// GET /tasks/:id - get one task
// POST /tasks - create task
// PUT /tasks/:id - update task
// DELETE /tasks/:id - delete task

// tasks.service.ts
// tasks.controller.ts
// tasks.module.ts
```

<details>
<summary>✅ Solution</summary>

```typescript
// tasks.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';

interface Task {
    id: number;
    title: string;
    description: string;
    completed: boolean;
}

@Injectable()
export class TasksService {
    private tasks: Task[] = [];
    private idCounter = 1;
    
    findAll(): Task[] {
        return this.tasks;
    }
    
    findOne(id: number): Task {
        const task = this.tasks.find(t => t.id === id);
        if (!task) throw new NotFoundException(`Task ${id} not found`);
        return task;
    }
    
    create(data: { title: string; description: string }): Task {
        const task: Task = {
            id: this.idCounter++,
            ...data,
            completed: false,
        };
        this.tasks.push(task);
        return task;
    }
    
    update(id: number, data: Partial<Task>): Task {
        const task = this.findOne(id);
        Object.assign(task, data);
        return task;
    }
    
    remove(id: number): void {
        const index = this.tasks.findIndex(t => t.id === id);
        if (index === -1) throw new NotFoundException(`Task ${id} not found`);
        this.tasks.splice(index, 1);
    }
}

// tasks.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { TasksService } from './tasks.service';

@Controller('tasks')
export class TasksController {
    constructor(private tasksService: TasksService) {}
    
    @Get()
    findAll() {
        return this.tasksService.findAll();
    }
    
    @Get(':id')
    findOne(@Param('id') id: string) {
        return this.tasksService.findOne(parseInt(id));
    }
    
    @Post()
    create(@Body() data: { title: string; description: string }) {
        return this.tasksService.create(data);
    }
    
    @Put(':id')
    update(@Param('id') id: string, @Body() data: any) {
        return this.tasksService.update(parseInt(id), data);
    }
    
    @Delete(':id')
    remove(@Param('id') id: string) {
        this.tasksService.remove(parseInt(id));
        return { message: 'Task deleted' };
    }
}

// tasks.module.ts
import { Module } from '@nestjs/common';
import { TasksController } from './tasks.controller';
import { TasksService } from './tasks.service';

@Module({
    controllers: [TasksController],
    providers: [TasksService],
})
export class TasksModule {}
```
</details>

---

# 📊 Quick Reference

## Difficulty Summary
| Level | Count | Topics |
|-------|-------|--------|
| 🟢 Easy | 20 | Basic syntax, simple forms, selectors |
| 🟡 Medium | 22 | Events, hooks, layouts, navigation |
| 🔴 Hard | 8+ | Complete apps, Context API, full CRUD |

## Topic Coverage
| Topic | Exercises |
|-------|-----------|
| HTML5 | 1-8 |
| CSS3 | 9-16 |
| JavaScript | 17-25 |
| React | 26-36 |
| Flutter | 37-45 |
| Node.js/NestJS | 46-50 |

---

**Good luck on your exam! 🍀**

*Tip: Practice these exercises without looking at solutions first, then check your answers!*

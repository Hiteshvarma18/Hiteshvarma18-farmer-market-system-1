const API =
"http://127.0.0.1:8000";

async function loadMarkets(){

const response =
await fetch(
API +
"/api/location/markets"
);

const data =
await response.json();

const market =
document.getElementById(
"market"
);

data.forEach(item=>{

market.innerHTML +=
`
<option value="${item.market}">
${item.market}
</option>
`;

});

}

async function loadPrices(){

const market =
document.getElementById(
"market"
).value;

const search =
document.getElementById(
"search"
).value.toLowerCase();

const response =
await fetch(
`${API}/api/location/prices?market=${market}`
);

const rows =
await response.json();

let html = "";

rows.forEach(item=>{

if(
search &&
!item.crop
.toLowerCase()
.includes(search)
){
return;
}

html += `
<div class="card">

<div class="crop">
${item.crop}
</div>

<div class="market">
${item.market}
</div>

<div class="price">
₹${item.price}
</div>

<div>
${item.date}
</div>

<a href="
market_details.html
?crop=${item.crop}
">
View Details
</a>

</div>
`;

});

document.getElementById(
"results"
).innerHTML =
html;

}

loadMarkets();
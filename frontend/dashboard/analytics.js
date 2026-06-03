const API =
"http://127.0.0.1:8000/api/analytics";

async function loadAnalytics(){

const response =
await fetch(
API + "/summary"
);

const data =
await response.json();

users.innerText =
data.users;

crops.innerText =
data.crops;

markets.innerText =
data.markets;

avg.innerText =
"₹" +
Number(
data.avg_price || 0
).toFixed(2);

high.innerHTML =
`${data.highest.crop}
(₹${data.highest.price})`;

low.innerHTML =
`${data.lowest.crop}
(₹${data.lowest.price})`;

}

loadAnalytics();
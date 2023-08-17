async function fetchData() {
    try {
        const fetch = (await import('node-fetch')).default;
        const response = await fetch('http://localhost:5000/v2/Destiny%202/all');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetchData();

async function main(){
	var ctx = document.getElementById('myChart').getContext('2d');

	const response = await fetch('http://127.0.0.1:5500/data/results.csv');
	const data = await response.text();


	let cols = [];
	let alt = [];

	const rows = data.split('\n').slice(1);

	let xlabels = [];
	for(let i = 0; i < rows.length; i++){
		xlabels.push(i);
	}


	for(let i = 0; i < rows[0].split(',').length; i++){
		cols.push([]);
	}

	rows.forEach(elt => {
		row = elt.split(',');
		for(let i = 0; i < row.length; i++){
			cols[i].push(Number(row[i]));
			if(i == 1){
				alt.push(parseFloat(row[i]));
			}
		}
	})
	
	console.log(cols[3]);


	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: xlabels,
			datasets: [
				{
					label: 'Altitude',
					data: alt,
					backgroundColor: ['rgba(255, 99, 132, 0.2)'],
					borderColor: ['rgba(255, 99, 132, 1)'],
					borderWidth: 1
				}
			]
		}
	});
}

main();
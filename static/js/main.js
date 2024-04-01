const margin = {top: 25, bottom: 75, left: 50, right: 50}

function plotErrorBars(svg, data, width, height, x_scale, title, control_mean, control_se, color='#74c476'){
    x_scale.range([0,width]);
    console.log(data.map(d => d.method))
    let y_scale = d3.scaleBand().domain(['vas', 'outlier', 'maxmin', 'random', 'blue']).range([height,0]).padding(1);

    svg.append('g')
        .selectAll('gridlines')
        .data(data)
            .enter()
            .append('line')
            .attr('transform', `translate(${margin.left},${margin.top})`)
                .attr('y1', d => y_scale(d.method))
                .attr('y2', d => y_scale(d.method))
                .attr('x1', 0)
                .attr('x2', width)
                .attr('stroke', 'lightgrey')
                .style("stroke-dasharray", ("3, 3"))

    let control = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)

    control.append('rect')
        .attr('y', -10)
        .attr('height', height+20)
        .attr('x', x_scale(control_mean-control_se))
        .attr('width', x_scale(2*control_se))
        .attr('fill', 'lightgrey')
        .style('opacity', 0.5)

    control.append('line')
        .attr('x1', x_scale(control_mean))
        .attr('x2', x_scale(control_mean))
        .attr('y1', -10)
        .attr('y2', height+10)
        .attr('stroke', 'darkgrey')
    
    control.append('text')
        .attr('x', x_scale(control_mean))
        .attr('y', -13)
        .text('control')
        .attr('font-size', 10)
        .attr('text-anchor', 'middle')

    let A_groups = svg.append('g')
        .selectAll('dots')
        .data(data)
            .enter()
            .append('g')

    A_groups.append('line')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .attr('x1', d => x_scale(d.mean_error-d.std_error))
        .attr('x2', d => x_scale(d.mean_error+d.std_error))
        .attr('y1', d => y_scale(d.method))
        .attr('y2', d => y_scale(d.method))
        .attr('stroke', color)
        .attr('stroke-width', 3)

    A_groups.append('circle')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .attr('cx', d => x_scale(d.mean_error))
        .attr('cy', d => y_scale(d.method))
        .attr('r', 5)
        .style('stroke', color)
        .style('fill', color)

    svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top+height})`)
            .call(d3.axisBottom(x_scale).ticks(7))
    
    svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`)
            .call(d3.axisLeft(y_scale))

    // svg.append('text')
    //     .attr('x', (width+margin.left+margin.right)/2)
    //     .attr('y', margin.top/2)
    //     .text(title)
    //     .attr('font-size', 16)
    //     .attr('text-anchor', 'middle')
    
    let task = document.getElementById('task').value
    svg.append('text')
        .attr('x', (margin.left+width+margin.right)/2)
        .attr('y', height + margin.top + margin.bottom/2)
        .text((task == 'filter') ? 'Precision and Recall' : (task == 'order') ? 'Kendall Tau' : 'Mean Error')
        .attr('font-size', 16)
        .attr('text-anchor', 'middle')

}

function plotBar(svg, data, width, height, title, control_percentage, colors=['#006d2c', '#74c476', '#a1d99b', '#c7e9c0', '#e5f5e0']){
    let x_scale = d3.scaleLinear().domain([0,100]).range([0,width]);
    let y_scale = d3.scaleBand().domain(['vas', 'outlier', 'maxmin', 'random', 'blue']).range([height,0]).padding([1]);
    
    svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .append('line')
            .attr('x1', x_scale(control_percentage))
            .attr('x2', x_scale(control_percentage))
            .attr('y1', -10)
            .attr('y2', height+10)
            .attr('stroke', 'darkgrey')

    svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .append('text')
        .attr('x', x_scale(control_percentage+0.5))
        .attr('y', 0)
        .text('control')
        .attr('font-size', 10)
        .attr('text-anchor', 'start')

    for(let i = colors.length; i > 0; i--){
        svg.append('g')
            .selectAll('dots')
            .data(data)
                .enter()
                    .append('rect')
                        .attr('transform', `translate(${margin.left},${margin.top})`)
                        .attr('x', 0)
                        .attr('width', d => {
                            console.log(i+2, d[`percentage_${i+2}`])
                            return x_scale(d[`percentage_${i+2}`])
                        })
                        .attr('y', d => y_scale(d.method)-5)
                        .attr('height', 10)
                        .style('fill', colors[i])
    }

    

    svg.append('g')
        .selectAll('dots')
        .data(data)
            .enter()
                .append('rect')
                    .attr('transform', `translate(${margin.left},${margin.top})`)
                    .attr('x', 0)
                    .attr('width', d => x_scale(d.percentage_correct))
                    .attr('y', d => y_scale(d.method)-5)
                    .attr('height', 10)
                    .style('fill', colors[0])
                
    

    svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top+height})`)
            .call(d3.axisBottom(x_scale))
    
    svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`)
            .call(d3.axisLeft(y_scale))

    // svg.append('text')
    //     .attr('x', (width+margin.left+margin.right)/2)
    //     .attr('y', margin.top/2)
    //     .text(title)
    //     .attr('font-size', 16)
    //     .attr('text-anchor', 'middle')

    svg.append('text')
        .attr('x', (margin.left+width+margin.right)/2)
        .attr('y', height + margin.top + margin.bottom/2)
        .text('Percentage of Answers Correct')
        .attr('font-size', 16)
        .attr('text-anchor', 'middle')

}

function refresh(){
    let condition_A = d3.select('#condition_A')
    let condition_B = d3.select('#condition_B')

    condition_A.selectAll('*').remove()
    condition_B.selectAll('*').remove()

    let width_A = condition_A.node().getBoundingClientRect().width - (margin.left + margin.right)
    let height_A = condition_A.node().getBoundingClientRect().height - (margin.top + margin.bottom)
    let width_B = condition_B.node().getBoundingClientRect().width - (margin.left + margin.right)
    let height_B = condition_B.node().getBoundingClientRect().height - (margin.top + margin.bottom)

    condition_A.append('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', width_A+(margin.left + margin.right))
        .attr('height', height_A+(margin.top + margin.bottom))
        .attr('fill', 'white')
        .attr('stroke', 'white')
    
    condition_B.append('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', width_B+(margin.left + margin.right))
        .attr('height', height_B+(margin.top + margin.bottom))
        .attr('fill', 'white')
        .attr('stroke', 'white')

    d3.csv('static/experiment-2-aggregate.csv', function(row){
        row.std_error = +row.std_error;
        row.mean_error = +row.mean_error;
        row.percentage_correct = +row.percentage_correct;
        row.percentage_3 = +row.percentage_3;
        row.percentage_4 = +row.percentage_4;
        row.percentage_5 = +row.percentage_5;
        row.percentage_6 = +row.percentage_6;
        return row
    }).then(function(data){
        let task = document.getElementById('task').value

        data_A = data.filter(d => d.condition == 'A' && d.task == task)
        data_B = data.filter(d => d.condition == 'B' && d.task == task)
        data_C = data.filter(d => d.condition == 'C' && d.task == task)[0]
        console.log(data_C)

        if (task == 'distribution' || task == 'anomalies'){
            plotBar(condition_A, data_A, width_A, height_A, 'Condition A', data_C.percentage_correct)
            plotBar(condition_B, data_B, width_B, height_B, 'Condition B', data_C.percentage_correct, ['#a63603', '#fd8d3c', '#fdae6b', '#fdd0a2', '#fee6ce'])
        }
        else{
            let x_scale = d3.scaleLinear()
                    .domain((task == 'filter' || task == 'order') 
                    ? [0.0,1.0]
                    : [
                        0,
                        d3.max(data.filter(d => d.task == task).map(d => d.mean_error+d.std_error))
                    ])

            plotErrorBars(condition_A, data_A, width_A, height_A, x_scale, 'Condition A', data_C.mean_error, data_C.std_error)
            plotErrorBars(condition_B, data_B, width_B, height_B, x_scale, 'Condition B', data_C.mean_error, data_C.std_error, '#fd8d3c')
        }
        

    })
}

function save_image_A(){
    let task = document.getElementById('task').value;
    let filename_A = `${task}_A.png`;
    saveSVGImage(d3.select(`#condition_A`), filename_A)
    
}

function save_image_B(){
    let task = document.getElementById('task').value;
    let filename_B = `${task}_B.png`;
    saveSVGImage(d3.select(`#condition_B`), filename_B)
}

window.onload = function(){
    refresh()
}
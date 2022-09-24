function close_total_calculation() {
    let share = parseFloat(document.getElementById('sharenumber').value);
    let avg = parseFloat(document.getElementById('avgp').value);
    let commission_fee = parseFloat(document.getElementById('commission').value);
    var total = share * avg - commission_fee;
    // document.getElementById('commission').value = parseFloat(commission_fee).toFixed(2);
    document.getElementById('costb').value = parseFloat(total).toFixed(2);
}

function total_calculation() {
    let share = parseFloat(document.getElementById('sharenumber').value);
    let avg = parseFloat(document.getElementById('avgp').value);
    let commission_fee = parseFloat(document.getElementById('commission').value);
    let transaction = document.getElementById("transaction_type");
    let type = transaction.options[transaction.selectedIndex].text;
    if (type === 'Buy') {
        var total = share * avg + commission_fee;
    } else {
        var total = share * avg - commission_fee;
    }
    // document.getElementById('commission').value = parseFloat(commission_fee).toFixed(2);
    document.getElementById('costb').value = parseFloat(total).toFixed(2);
}
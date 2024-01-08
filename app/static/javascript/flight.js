function addFlightToCart(id, company_name,route_name ,aircraft_name,
 aircraft_id,seat_class_id ,seat_class_name, departure_time, price, company_logo){
    fetch('/api/cart', {
        method: 'post',
        body: JSON.stringify({
            'id':id,
            'aircraft_id': aircraft_id,
            'aircraft_name':aircraft_name,
            'route_name' : route_name,
            'company_name': company_name,
            'seat_class_id':seat_class_id,
            'seat_class_name': seat_class_name,
            'departure_time': departure_time,
            'company_logo': company_logo,
            'price': price
        }),
        headers : {
            'Content-Type': 'application/json'
        }
    })
    .then(function(response){
        return response.json()
    })
    .then(function(result){
        tickets = result['tickets']
        costs = result['total_cost']['total_price']
        loadTicket(tickets, costs)
    })
 }

function removeFlight(flight_id, sc_id){
   fetch(`/api/cart/flight${flight_id}/${sc_id}`, {
       method: 'delete'
   })
   .then(function(response){
       return response.json()
   })
   .then(function(result){
       tickets = result['tickets']
       costs = result['total_cost']['total_price']
       loadTicket(tickets, costs)
   })
}

function loadTicket(tickets, costs){
    var parentDiv = document.getElementById("parentDiv");
    parentDiv.innerHTML = ''
    for(ticket in tickets){
        ticket = tickets[ticket]
        for(var sc_id in ticket.seat_class){
            var sc = ticket.seat_class[sc_id]

            var flightDiv = document.createElement("div");
            flightDiv.className = 'flight-item'
            parentDiv.appendChild(flightDiv);
            var titleDiv = document.createElement("div")
            titleDiv.className = 'titleDiv'
            titleDiv.innerHTML = `
            <img class="company-logo" src= "${ticket.company_logo}"></img>
            <h2>${ticket.company_name}</h2>
            <p id="price-p">Giá: ${sc.price} VND</p>
            `;
            flightDiv.appendChild(titleDiv)
            var btnDel = document.createElement("button")
            btnDel.setAttribute('onclick', `removeFlight(${ticket.id},${sc_id})`)
            btnDel.innerHTML = `<i class="fas fa-times"></i>`
            flightDiv.appendChild(btnDel)

            var seatDiv = document.createElement("div");
            seatDiv.id = `seat${ticket.id}_${sc_id}`;
            seatDiv.innerHTML = `
                <p>Mã máy bay: ${ticket.aircraft_name}</p>
                <p>Trạng thái: Còn chỗ</p>
                <p>Hạng ghế: ${sc.seat_class_name}</p>
            `;
            var dateDiv = document.createElement("div")
            dateDiv.className = "date-div"
            dateDiv.innerHTML = `
                <p>12:22</p>
                <p>12/12/2002</p>
            `

            var bigDiv = document.createElement("div")
            bigDiv.className = "big-div"
            bigDiv.appendChild(seatDiv)
            bigDiv.appendChild(dateDiv)

            flightDiv.appendChild(bigDiv);


            var quantityOpt = document.createElement("div")
            quantityOpt.className = "quantityOpt"
            quantityOpt.innerHTML = `
                <p>Số lượng: </p>
                <input value=${sc.quantity} type="number" id="quantity-ticket" min="1" max="10">
            `
            flightDiv.appendChild(quantityOpt)
        }
    }
    var text_price = document.getElementById('text-price')
    var flight_items = document.getElementsByClassName('flight-item')
    console.log(flight_items.length)
    if(flight_items.length == 0){
        var text_none = document.createElement("div")
        text_none.innerHTML = `
            <p>Ban chua co ve nao :((</p>
        `
        parentDiv.appendChild(text_none)
        text_price.innerHTML = "0đ"
    }
    else{
        text_price.innerHTML = `${costs}đ`
    }
 }

function pay(){
    fetch("/api/pay", {
        method: "post"
    })
    .then(function(response){
        return response.json()
    })
    .then(function(result){
        console.log(result)
        if(result['list_ticket'].length == 0){
            alert("Ban chua dat ve!")
        }
        else{
            alert("Dat ve thanh cong!")
        }
    })
}

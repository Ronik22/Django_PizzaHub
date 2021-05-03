document.querySelectorAll(".quantity").forEach(qty => qty.addEventListener("change", changeSubtotal));
    document.querySelector('body').onload = function() {
        var container = document.getElementsByClassName('quantity');
        for(var i=0; i<container.length; i++) {
            console.log(container[i]);
            changeSubtotalOnLoad(container[i]);
        }
        total();
    };


    // Change subtotal
    function changeSubtotal(element) {
        var price = this.previousElementSibling.innerHTML;
        var quantity = element.target.value; 
        var subtotal = parseFloat(price * quantity).toFixed(2);
        this.nextElementSibling.innerHTML = subtotal;
        total();
    }

    // Change subtotal on load
    function changeSubtotalOnLoad(element) {
        var price = element.previousElementSibling.innerHTML;
        var quantity = element.getElementsByTagName('input')[0].value; 
        var subtotal = parseFloat(price * quantity).toFixed(2);
        element.nextElementSibling.innerHTML = subtotal;
    }

    // Sum total
    function total(){
        var totalDisplay = document.getElementById("total_display");
        var totalDisplay2 = document.getElementById("total_display2");
        var endtotalDisplay = document.getElementById("endtotal_display");
        var totalQuantity = document.getElementById("total_quantity");
        var delvCharges = document.getElementById("delv_charges");

        var sum = 0;
        var noitems = 0;
        var tbody = document.getElementById("all_products");

        for (var i = 0; i < tbody.rows.length; i++) {
            sum = sum + parseFloat(tbody.rows[i].cells[3].innerHTML);
            noitems = noitems + parseInt(tbody.rows[i].cells[2].getElementsByTagName('input')[0].value);
        }
        var total = sum.toFixed(2);
        totalDisplay.innerHTML =  "₹"+total;
        totalDisplay2.innerHTML = total;
        totalQuantity.innerHTML = noitems;
        endtotalDisplay.innerHTML = (parseFloat(total)+parseFloat(delvCharges.innerText)).toFixed(2);
    }

    function checkoutp(){
        var tbody = document.getElementById("all_products");
        var cfs = document.getElementById("checkoutfs");
        var pdict = {};

        for (var i = 0; i < tbody.rows.length; i++) {
            PID = tbody.rows[i].cells[0].getElementsByClassName('pid')[0].innerText;
            noitems = tbody.rows[i].cells[2].getElementsByTagName('input')[0].value;
            pdict[PID] = noitems;
        }
        cfs.getElementsByTagName('input')[1].value = JSON.stringify(pdict);
        console.log(JSON.stringify(pdict));
        cfs.submit();
    }
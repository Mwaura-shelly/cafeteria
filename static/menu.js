const cartItems = document.querySelector("#cart-items");
const emptyCart = document.querySelector(".empty-cart");
const placeOrder = document.querySelector("#place-order");

function updateCart(item) {
    const name = item.dataset.name;
    const price = Number(item.dataset.price);
    const quantity = Number(item.querySelector(".quantity").textContent);

    let cartItem = [...cartItems.children]
        .find((entry) => entry.dataset.name === name);

    if (quantity === 0) {
        cartItem?.remove();
    } else if (!cartItem) {
        cartItem = document.createElement("li");
        cartItem.dataset.name = name;
        cartItems.appendChild(cartItem);
    }

    if (cartItem) {
        cartItem.textContent =
            `${name} x ${quantity} - KSh ${price * quantity}`;
    }

    emptyCart.hidden = cartItems.children.length > 0;
    placeOrder.disabled = cartItems.children.length === 0;
}

function updateAvailability(item) {
    const availability = item.querySelector(".availability");

    if (!availability) {
        return;
    }

    const stock = Number(item.dataset.quantity);
    const ordered = Number(item.querySelector(".quantity").textContent);

    const remaining = stock - ordered;

    availability.textContent = `Available: ${remaining}`;
}

document.querySelectorAll("li").forEach((item) => {

    const quantity = item.querySelector(".quantity");
    const plusButton = item.querySelector(".plus");
    const minusButton = item.querySelector(".minus");

    if (!quantity || !plusButton || !minusButton) {
        return;
    }

    const available = Number(item.dataset.available);
    const stock = Number(item.dataset.quantity);

    // If admin marked the food as unavailable
    if (available === 0) {
        plusButton.disabled = true;
        minusButton.disabled = true;
        item.classList.add("unavailable");
        return;
    }


    plusButton.addEventListener("click", () => {

        const currentQuantity = Number(quantity.textContent);

        // Foods with a stock quantity
        if (stock > 0 && currentQuantity >= stock) {
            return;
        }

        quantity.textContent = currentQuantity + 1;

        updateAvailability(item);
		updateCart(item);

    });


    minusButton.addEventListener("click", () => {

        const currentQuantity = Number(quantity.textContent);

        quantity.textContent = Math.max(
            0,
            currentQuantity - 1
        );
        
		updateAvailability(item);
		updateCart(item);
    });
    placeOrder.addEventListener("click", () => {

    const items = [...cartItems.children]
        .map(item => item.textContent)
        .join(", ");

    const total = [...cartItems.children]
        .reduce((sum, item) => {

            const price = Number(
                item.textContent.match(/KSh (\d+)/)[1]
            );

            return sum + price;

        }, 0);

    const form = document.createElement("form");

    form.method = "POST";
    form.action = "/place-order";

    const itemsInput = document.createElement("input");
    itemsInput.type = "hidden";
    itemsInput.name = "items";
    itemsInput.value = items;

    const totalInput = document.createElement("input");
    totalInput.type = "hidden";
    totalInput.name = "total";
    totalInput.value = total;

    form.appendChild(itemsInput);
    form.appendChild(totalInput);

    document.body.appendChild(form);

    form.submit();
});

});
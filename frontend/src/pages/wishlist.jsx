import { Component } from 'react'
import axios from 'axios';
const token=localStorage.getItem("token");

class Wishlist extends Component {
    state = {
        products: [],
        productData: {
            productName: "",
            productPrice: ""
        }
    }

    getWishlistParam = new URLSearchParams();


    render(){
        return(
            <div>
               BRAVO BOSSULE
            </div>
        )
    }
}

export default Wishlist
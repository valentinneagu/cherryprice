import React, { Component } from 'react';
import './index.css'
import logo from './cherries.svg';
import {Link } from 'react-router-dom';
import axios from 'axios';
import { Modal, Button, Form } from 'react-bootstrap';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';
import Wishlist from './wishlist'
const token=localStorage.getItem("token");


class MainMenu extends Component {

    state = {
        wishlists: [],
        newWatchhListData: {
            watchlistName: ""
        },
        isOpenAddWishlist:false,
        wishListModal: false,
        modalTitle: "",
        wishListId:"",
        products: []
    }

    componentWillMount() {
        this.getWatchlists()
    }

    basestate = {
        wishlists: [],
        newWatchhListData: {
            watchlistName: ""
        },
        isOpenAddWishlist:false,
        wishListModal: true
    }


    redirectWishlist = () => {
        this.setState({wishListPage: true})
        this.renderWishlistPage();
      }

    renderWishlistPage = () => {
        if(this.state.wishListPage) {
          return <Redirect to={{pathname: '/wishlist',
                                state: {cookie: this.cookies}}}/>
        }
      }

    openWishListModal = () => this.state({wishListModal: true})
    closeWishListModal = () => this.state({wishListModal: false})
    
    watchListParam = new URLSearchParams();
    getWishlistParam = new URLSearchParams();

    getWatchlists() {
        axios.defaults.headers.common['Authorization'] = token;
        axios.get("http://localhost:5000/dashboard")
        .then(res => {
            console.log(JSON.parse(JSON.stringify(res.data)));
            this.setState({
                wishlists: JSON.parse(JSON.stringify(res.data))
            })
        });
    }

    addWatchList(e) {
        this.setState(this.state.newWatchhListData);
        this.watchListParam.append('watchlist_name', this.state.newWatchhListData.watchlistName);
        e.preventDefault();
        axios.defaults.headers.common['Authorization'] = token;
        axios.post("http://localhost:5000/addwatchlist", this.watchListParam)
             .then(res => {console.log(res)})
             .then(this.closeAddModal)
             .then(this.deleteStateAndParam)
    }

    deleteStateAndParam = () => {
        this.setState(this.basestate);
        this.watchListParam.delete('watchlist_name');
    }

    getWatchList() {
        this.getWishlistParam.append('id', this.state.wishListId);
        axios.defaults.headers.common['Authorization'] = token;
        axios.post("http://localhost:5000/watchlist", this.getWishlistParam)
             .then(res=>{this.setState({products: res.data})})
    }

    openAddModal = () => this.setState({isOpenAddWishlist: true});
    closeAddModal = () => this.setState({isOpenAddWishlist: false});
    render() {
        
        return (
            <Router>
                <div>
                {/* {this.getWatchlists()} */}
                    <Route exact path="/menu">
                <header className="menuHeader">
                <img src={logo} className="logo" alt="logo" />
                    <b className="menuTitle">Cherry Price</b>
                    <Link to="/" className="logoutbtn">Log Out</Link>
                </header>
                <div className="menuBody">
                    <p className="dashboard">
                        Dashboard
                    </p>
                    <div>
                        {
                            this.state.wishlists.map(element => {
                                return(
                                <div className="boxedbox" key={element}>
                                <button className="eleButton" onClick={() => {this.setState({wishListModal: true});
                                                                            this.setState({modalTitle: element.name});
                                                                            this.setState({wishListId: element.id});
                                                                            this.getWatchList()}}>{element.name}</button>
                            </div>
                            )
                            })
                        }
                    </div>
                    <button className="button newWishlist" onClick={this.openAddModal}>Add new watchlist</button>
                        <Modal show={this.state.isOpenAddWishlist} className="addWatchMdl">
                            <Form onSubmit={this.addWatchList.bind(this)}>
                                <Modal.Header closeButton>
                                    <Modal.Title>
                                        Wishlist
                                    </Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <p>
                                        <input type="text"
                                               id="newwatchlistname"
                                               value={this.state.newWatchhListData.watchlistName}
                                               onChange={e => {
                                                   let {newWatchhListData} = this.state;

                                                   newWatchhListData.watchlistName = e.target.value;

                                                   this.setState({newWatchhListData});
                                               }}
                                               placeholder="Watchlist name">
                                               </input>
                                    </p>
                                </Modal.Body>
                                <Modal.Footer>
                                    <Button type="submit">
                                        Add Watchlist
                                    </Button>
                                    <Button onClick={this.closeAddModal}>
                                        Cancel
                                    </Button>
                                </Modal.Footer>
                            </Form>
                        </Modal>
             
                </div>

                <Modal show={this.state.wishListModal} className="addWatchMdl">
                            
                            <Modal.Header closeButton>
                                <Modal.Title>
                                    {this.state.modalTitle}
                                </Modal.Title>
                            </Modal.Header>
                            <Modal.Body>
                                    {this.state.products}
                            </Modal.Body>
                            <Modal.Footer>

                                <Button onClick={() => {this.setState({wishListModal: false})}}>
                                    Cancel
                                </Button>
                            </Modal.Footer>
                    </Modal>
                </Route>

                <Route exact path="/wishlist" component={Wishlist}></Route>
                {this.renderWishlistPage()}
            </div>
            </Router>
        );
    }
}

export default MainMenu;
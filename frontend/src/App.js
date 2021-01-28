import logo from './cherries.svg';
import './App.css';
import { Component } from 'react';
import { Modal, Button, Form } from "react-bootstrap";
import axios from "axios";
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';
import MainMenu from "./pages";


class App extends Component {
  state = {
    users: [],
    newUserData: {
      username: "",
      password: ""
    },
    isOpenRegister: false,
    isOpenLogin: false,
    mainMenu: false
  };
  userParam = new URLSearchParams();
  basestate={
    users: [],
    newUserData: {
      username: "",
      password: ""
    },
    isOpenRegister: false,
    isOpenLogin: false,
    mainMenu: false
  };


  openLoginModal = () => this.setState({ isOpenLogin: true });
  closeLoginModal = () => this.setState({ isOpenLogin: false });
  openRegisterModal = () => this.setState({ isOpenRegister: true });
  closeRegisterModal = () => this.setState({ isOpenRegister: false });
  
  redirectHandler = () => {
    this.setState({mainMenu: true})
    this.renderMenu();
  }

  renderMenu = () => {
    if(this.state.mainMenu) {
      return <Redirect to={{pathname: '/menu',
                            state: {cookie: this.cookies}}}/>
    }
  }
  config = {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }

  addUser(e) {
    this.setState(this.state.newUserData);
    this.userParam.append('username', this.state.newUserData.username);
    this.userParam.append('password', this.state.newUserData.password);
    e.preventDefault();
    axios.post("http://localhost:5000/register", this.userParam)
         .then(res => {console.log(res);console.log(res.data);})
         .then(this.closeRegisterModal)
         .then(this.cancelStateAndParam)
  }

  loginUser(e) {
    this.setState(this.state.newUserData);
    this.userParam.append('username', this.state.newUserData.username);
    this.userParam.append('password', this.state.newUserData.password);
    e.preventDefault();
    axios.post("http://localhost:5000/login", this.userParam).then(res => {console.log(res);localStorage.setItem("token",res.data.token);console.log(localStorage.getItem("token"));console.log(res.data.expires_in);}).then(this.redirectHandler()).then(this.cancelStateAndParam)
  }
  cancelStateAndParam = () =>{
    this.setState(this.basestate);
    this.userParam.delete('username');
    this.userParam.delete('password');
  }
  render() {
    return (
      <Router><div className="App">
          <Route exact path="/">
          <div className="App-body">
            <img src={logo} className="App-logo" alt="logo" />
            <p className="App-name">
              Cherry Price
            </p>
            <Button variant="primary" onClick={this.openLoginModal} className="loginBtn">
              <p className="logintxt">Log In</p>
            </Button>
              <Modal show={this.state.isOpenLogin} onHide={this.closeLoginModal} className="loginModal">
                <Form onSubmit={this.loginUser.bind(this)}>
                <Modal.Header closeButton>
                  <Modal.Title>Log In</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  <p><input type="text"
                            id="username"
                            value={this.state.newUserData.username}
                            onChange={e => {
                              let {newUserData} = this.state;

                              newUserData.username = e.target.value;

                              this.setState({newUserData});
                            }} 
                            placeholder="Username"></input></p>
                  <input type="text"
                         id="password"
                         value={this.state.newUserData.password}
                         onChange={e => {
                           let {newUserData} = this.state;

                           newUserData.password = e.target.value;

                           this.setState({newUserData});
                           
                         }}
                         placeholder="Password"></input>
                </Modal.Body>
                <Modal.Footer>
                  <Button type="submit">
                    Log In
                  </Button>
                </Modal.Footer>
                </Form>
              </Modal>

              <Button variant="primary" onClick={this.openRegisterModal} className="registerBtn">
              <p className="registertxt">Register</p>
            </Button>
              <Modal show={this.state.isOpenRegister} onHide={this.closeRegisterModal} className="registerModal">
                  <Form onSubmit={this.addUser.bind(this)}>
                  <Modal.Header closeButton>
                  <Modal.Title>Register</Modal.Title>
                </Modal.Header>
                
                <Modal.Body>
                  <p><input type="text" 
                            id="username"
                            value={this.state.newUserData.username}
                            onChange={e => {
                              let {newUserData} = this.state;

                              newUserData.username = e.target.value;

                              this.setState({newUserData});
                            }}  placeholder="Username">
                  </input></p>
                  <p><input type="text" id="password" value={this.state.newUserData.password}
                            onChange={e => {
                              let {newUserData} = this.state;

                              newUserData.password = e.target.value;

                              this.setState({newUserData});
                              
                            }}  placeholder="Password"></input></p>
                  <input type="text" id="c_password" placeholder="Confirm Password"></input>
                  
                </Modal.Body>
                
                <Modal.Footer>
                  
                  <Button variant="secondary" onClick={this.cancelRegister}>
                    Cancel
                  </Button>
                  <Button type="submit">
                    Register
                  </Button>
                </Modal.Footer>
                  </Form>
              </Modal>
          </div>
          </Route>
          
          <Route exact path="/menu" component={MainMenu}/>
          {this.renderMenu()}
          
        </div>
      </Router>  
    );
  }
}

export default App;

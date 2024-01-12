import React, { useEffect, useState } from "react";

import Header from "./Header";
import ToyForm from "./ToyForm";
import ToyContainer from "./ToyContainer";
import Login from "./Login";
import UserDetails from "./UserDetails";

function App() {
  const [user, setUser] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [toys, setToys] = useState([]);

  useEffect(() => {
    fetch(`/check_session`).then((res) => {
        if (res.ok) {
            res.json().then((user) => setUser(user));
        }
    });
}, []);

  useEffect(() => {
    if (user) {
      fetch(`/users/${user.id}/toys`)
      .then((res)=> res.json())
      .then((data) => {
        if (data.length > 0) {
          setToys(data)
        }
      });
    }
  }, [user]);
  /**********************
        Authentication
    ************************/
  function attemptLogin(userInfo) {
    fetch(`/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accepts: "application/json"
      },
      body: JSON.stringify(userInfo)
    })
      .then((res)=> {
        if (res.ok) {
          return res.json();
        }
        throw res
      })
      .then((data)=> setUser(data))
      .catch((e) => console.log(e));
  }
  function logout() {
    fetch(`/logout`, { method: "DELETE"}).then((res) => {
      if (res.ok) {
        setUser(null);
      }
    });
  }

  function handleClick() {
    setShowForm((showForm) => !showForm);
  }

  function handleAddToy(newToy) {
    setToys([...toys, newToy]);
  }

  function handleDeleteToy(toyToDelete) {
    const updatedToys = toys.filter((toy) => toy.id !== toyToDelete.id);
    setToys(updatedToys);
  }

  function handleUpdateToy(updatedToy) {
    const updatedToys = toys.map((toy) =>
      toy.id === updatedToy.id ? updatedToy : toy
    );
    setToys(updatedToys);
  }

  return (
    <div>
      {user ? (
      <>
        <Header />
        <UserDetails currentUser={user} logout={logout} />
        {showForm ? <ToyForm onAddToy={handleAddToy} /> : null}
        <div className="buttonContainer">
          <button onClick={handleClick}>Add a Toy</button>
        </div>
        <ToyContainer
          toys={toys}
          onDeleteToy={handleDeleteToy}
          onUpdateToy={handleUpdateToy}
        />
      </>
      ) : (
        <Login attemptLogin={attemptLogin} />
    )}

    </div>
  );
}

export default App;
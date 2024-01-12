function UserDetails({currentUser, logout}) {

    return (
      <div className='user-details'>
        <h2>Welcome {currentUser?.name}!</h2>
        <button onClick={logout}>Logout</button>
      </div>
    )
  
  }
  
  export default UserDetails
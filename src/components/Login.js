import { useState } from 'react'

function Login({attemptLogin}) {

  // STATE //

  const [name, setName] = useState('')
  const [password, setPassword] = useState('')

  // EVENTS //

  const handleChangeUsername = e => setName(e.target.value)
  const handleChangePassword = e => setPassword(e.target.value)

  function handleSubmit(e) {
    e.preventDefault()
    attemptLogin({"name": name, "password":password})
  }

  // RENDER //

  return (
    <form className='user-form' onSubmit={handleSubmit}>

      <h2>Login</h2>

      <input type="text"
      onChange={handleChangeUsername}
      value={name}
      placeholder='name'
      />

      <input type="text"
      onChange={handleChangePassword}
      value={password}
      placeholder='password'
      />

      <input type="submit"
      value='Login'
      />

    </form>
  )

}

export default Login
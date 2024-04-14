import { useRef, useState } from "react";
import "./Register.css";
import "./Change_password.css";
import iconoImg from "../assets/logo.png";
import { Link } from "react-router-dom";
import axios from "../api/axios.jsx";
import Cookies from 'universal-cookie';

function Change_password() {
  const [formData, setFormData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: ""
  });

  const [errMsg, setErrMsg] = useState("");
  const errRef = useRef();

  const handleInput = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.newPassword !== formData.confirmPassword) {
      setErrMsg("Las contraseñas no coinciden.");
      return;
    }

    const cookies = new Cookies();
    const jwt = cookies.get("auth_token");

    try {
      const response = await axios.post("http://127.0.0.1:8000/update_password/", {
        jwt: jwt,
        password: formData.currentPassword,
        new_password: formData.newPassword,
        new_password_confirm: formData.confirmPassword
      });
      
      if (response.data.type === "SUCCESS") {
        // Contraseña cambiada con éxito
        alert(response.data.message + " Inicia sesión nuevamente" );
        cookies.remove("auth_token");
        // Aquí podrías redirigir al usuario a alguna página de éxito o mostrar un mensaje
        window.location.href = "http://localhost:5173/login";
      } else {
        // Mostrar mensaje de error del backend
        alert(response.data.message);
      }
    } catch (error) {
      console.error("Error al cambiar la contraseña:", error);
      //setErrMsg("Ocurrió un error al cambiar la contraseña. Por favor, inténtalo de nuevo.");
    }
  };

  return (
    <div className="register">
      <div className="form">
        <div className="icon">
          <img
            src={iconoImg}
            alt="Icono de la página"
            style={{ width: "45px", height: "50px" }}
          />
        </div>
        <h1>Crea tu nueva contraseña</h1>
        <h1
          ref={errRef}
          className={errMsg ? "errmsg li-h1-error " : "offscreen"}
          aria-live="assertive"
        >
          {errMsg}
        </h1>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="currentPassword">Contraseña actual</label>
            <input
              type="password"
              id="currentPassword"
              name="currentPassword"
              placeholder="Introduce tu contraseña actual"
              required
              onChange={handleInput}
            />
          </div>
          <div className="input-group">
            <label htmlFor="newPassword">Nueva contraseña</label>
            <input
              type="password"
              id="newPassword"
              name="newPassword"
              placeholder="Introduce tu nueva contraseña"
              required
              onChange={handleInput}
            />
          </div>
          <div className="input-group">
            <label htmlFor="confirmPassword">Confirmar contraseña</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              placeholder="Confirma tu nueva contraseña"
              required
              onChange={handleInput}
            />
          </div>
          <p className="note">
            Debe contener 8+ caracteres, incluyendo al menos 1 letra y 1 número.
          </p>
          <br />
          <button type="submit" className="register-button center-button">
            <strong>Cambiar contraseña</strong>
          </button>
        </form>
        <center>
          <p className="loginRegister">
            ¿Deseas volver a los datos de usuario <Link to={"/profile"}>Perfil</Link>
          </p>
        </center>
      </div>
    </div>
  );
}

export default Change_password;

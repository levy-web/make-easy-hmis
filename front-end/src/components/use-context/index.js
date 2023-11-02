import { useState, createContext, useEffect } from "react";
import { APP_API_URL } from "@/assets/api-endpoints";
import { useRouter } from "next/router";
import axios from "axios";
import jwtDecode from "jwt-decode";
import SimpleCrypto from "simple-crypto-js";
import { useDispatch } from "react-redux";
import { getAllUserPermissions } from "@/redux/features/auth";
import { toast } from 'react-toastify'


export const authContext = createContext();

const secretKey = new SimpleCrypto(process.env.NEXT_PUBLIC_ENCRYPTION_KEY);

export const AuthProvider = ({ children }) => {
  const dispatch = useDispatch();
  const router = useRouter();
  // const [user, setUser] = useState(null);
  const [user, setUser] = useState(() =>
    typeof window !== "undefined" && localStorage.getItem("token")
      ? JSON.parse(localStorage.getItem("token"))
      : null
  );

  console.log("PARSED_USER ",user)
  const [message, setMessage] = useState("");

  // login User
  const loginUser = async (email, password) => {
    try {
      const response = await axios.post(APP_API_URL.LOGIN, {
        email: email,
        password: password,
      });
      if (response.status === 200) {
        const decodedUser = jwtDecode(response.data.access);
        setUser({ ...decodedUser, token: response.data.access });
        try {
          // await dispatch(getAllUserPermissions(decodedUser?.user_id));
          // router.push("/dashboard");
          localStorage.setItem("token", JSON.stringify(response.data.access));
          localStorage.setItem(
            "refresh",
            JSON.stringify(response.data.refresh)
          );
          if (decodedUser?.role === "patient") {
            // router.push('/')
            router.push(`/patient-profile`);
          }else{
            router.push('/dashboard')
          }
        } catch (error) {
          throw error;
        }
      }
    } catch (error) {
      toast.error(error.response.data.non_field_errors[0]);
    }
  };

  // logout User
  const logoutUser = () => {
    // setAuthToken(null);
    setUser(null);
    localStorage.removeItem("token");
    router.push("/auth/login");
  };

  let contextData = {
    loginUser: loginUser,
    message: message,
    logoutUser: logoutUser,
    user: user,
  };

  // decode the token and set the user when a component mounts
  useEffect(() => {
    const storedToken = JSON.parse(localStorage.getItem("token"));
    let decodedToken;
    if (storedToken) {
      decodedToken = jwtDecode(storedToken);

      setUser({ ...decodedToken, token: storedToken });
    }
    // const fetchPermissions = async () => {
    //   if (decodedToken) {
    //     await dispatch(getAllUserPermissions(decodedToken.user_id));
    //   }
    // };
    // fetchPermissions();
  }, []);

  return (
    <authContext.Provider value={contextData}>{children}</authContext.Provider>
  );
};

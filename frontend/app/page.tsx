"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/stores/authStore";
import LoginForm from "@/components/LoginForm";
import Header from "@/components/Header";
import PokemonGrid from "@/components/PokemonGrid";

export default function Home() {
  const { isAuthenticated, checkAuth, isLoading } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isLoading) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", minHeight: "100vh" }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return (
    <>
      <Header />
      <PokemonGrid />
    </>
  );
}

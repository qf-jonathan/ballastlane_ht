"use client";

import { useAuthStore } from "@/stores/authStore";
import styles from "./Header.module.css";

export default function Header() {
  const { user, logout } = useAuthStore();

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <h1 className={styles.title}>Pokédex</h1>
        {user && (
          <div className={styles.userSection}>
            <span className={styles.username}>Welcome, {user.username}</span>
            <button onClick={logout} className={styles.logoutButton}>
              Sign Out
            </button>
          </div>
        )}
      </div>
    </header>
  );
}

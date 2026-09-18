// SPDX-License-Identifier: MIT

import { create } from 'zustand';
import type { User, UserMeta } from '../types';
import { getUserMeta, setUserMeta } from './storage';

interface UserStore {
  currentUser: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  userMetadata: UserMeta | null;
  setCurrentUser: (user: User | null) => void;
  setUserMetadata: (meta: UserMeta) => void;
  setIsLoading: (loading: boolean) => void;
  clearAuth: () => void;
  hydrate: () => Promise<void>;
}

export const useUserStore = create<UserStore>((set) => ({
  currentUser: null,
  isAuthenticated: false,
  isLoading: true,
  userMetadata: null,

  setCurrentUser: (user) => {
    set({
      currentUser: user,
      isAuthenticated: !!user,
      isLoading: false,
    });
    if (user) {
      const meta = getUserMeta();
      set({ userMetadata: meta });
    }
  },

  setUserMetadata: (meta) => {
    set({ userMetadata: meta });
    setUserMeta(meta);
  },

  setIsLoading: (loading) => {
    set({ isLoading: loading });
  },

  clearAuth: () => {
    set({
      currentUser: null,
      isAuthenticated: false,
      isLoading: false,
      userMetadata: null,
    });
  },

  hydrate: async () => {
    try {
      if (typeof window !== 'undefined') {
        const meta = getUserMeta();
        set({ userMetadata: meta });
      }
      set({ isLoading: false });
    } catch (err) {
      console.error('Hydrate error:', err);
      set({ isLoading: false });
    }
  },
}));

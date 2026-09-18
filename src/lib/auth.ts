// SPDX-License-Identifier: MIT

import { supabase } from './supabase';
import type { User } from '../types';

export async function signup(email: string, password: string, displayName?: string): Promise<User | null> {
  try {
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email,
      password,
    });

    if (authError || !authData.user) {
      console.error('Signup error:', authError);
      return null;
    }

    const user: User = {
      id: authData.user.id,
      email: authData.user.email || '',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      profile: {
        displayName: displayName || email.split('@')[0],
      },
    };

    return user;
  } catch (err) {
    console.error('Signup exception:', err);
    return null;
  }
}

export async function login(email: string, password: string): Promise<User | null> {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error || !data.user) {
      console.error('Login error:', error);
      return null;
    }

    const user: User = {
      id: data.user.id,
      email: data.user.email || '',
      createdAt: data.user.created_at ? new Date(data.user.created_at).getTime() : Date.now(),
      updatedAt: Date.now(),
      profile: {
        displayName: data.user.user_metadata?.displayName || email.split('@')[0],
        avatarUrl: data.user.user_metadata?.avatarUrl,
        bio: data.user.user_metadata?.bio,
      },
    };

    return user;
  } catch (err) {
    console.error('Login exception:', err);
    return null;
  }
}

export async function logout(): Promise<boolean> {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error('Logout error:', error);
      return false;
    }
    return true;
  } catch (err) {
    console.error('Logout exception:', err);
    return false;
  }
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
      return null;
    }

    return {
      id: user.id,
      email: user.email || '',
      createdAt: user.created_at ? new Date(user.created_at).getTime() : Date.now(),
      updatedAt: Date.now(),
      profile: {
        displayName: user.user_metadata?.displayName || user.email?.split('@')[0],
        avatarUrl: user.user_metadata?.avatarUrl,
        bio: user.user_metadata?.bio,
      },
    };
  } catch (err) {
    console.error('Get current user exception:', err);
    return null;
  }
}

export async function onAuthStateChange(callback: (user: User | null) => void): Promise<() => void> {
  const { data: { subscription } } = supabase.auth.onAuthStateChange(async (_event, session) => {
    if (session?.user) {
      const user: User = {
        id: session.user.id,
        email: session.user.email || '',
        createdAt: session.user.created_at ? new Date(session.user.created_at).getTime() : Date.now(),
        updatedAt: Date.now(),
        profile: {
          displayName: session.user.user_metadata?.displayName || session.user.email?.split('@')[0],
          avatarUrl: session.user.user_metadata?.avatarUrl,
          bio: session.user.user_metadata?.bio,
        },
      };
      callback(user);
    } else {
      callback(null);
    }
  });

  return () => subscription?.unsubscribe();
}

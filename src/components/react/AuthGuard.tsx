// SPDX-License-Identifier: MIT

import React, { useEffect, useState } from 'react';
import { useUserStore } from '../../lib/userStore';
import { getCurrentUser } from '../../lib/auth';

interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export default function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { currentUser, isLoading, setCurrentUser } = useUserStore();
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const initAuth = async () => {
      const user = await getCurrentUser();
      setCurrentUser(user);
      setHydrated(true);
    };
    initAuth();
  }, [setCurrentUser]);

  if (!hydrated || isLoading) {
    return fallback || <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!currentUser) {
    return fallback || (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <h1 className="text-2xl font-bold">Please log in</h1>
        <a href="/auth/login" className="text-accent hover:underline">
          Go to login page
        </a>
      </div>
    );
  }

  return <>{children}</>;
}

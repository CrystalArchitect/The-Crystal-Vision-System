// SPDX-License-Identifier: MIT

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error('Supabase URL and anonymous key are required. Check your .env file.');
}

export const supabase = createClient(supabaseUrl, supabaseKey);

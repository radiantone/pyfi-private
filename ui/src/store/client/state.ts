export interface UserStateInterface {
  logged_in: boolean;
}

function state (): UserStateInterface {
  return {
    logged_in: false,
  };
}

export default state;

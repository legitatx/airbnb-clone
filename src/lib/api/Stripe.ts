import stripe from "stripe";

const client = new stripe(
  "sk_test_51IDYu2DPA2EfKp5HW2iSg6ZUxTozglkN6DqNkss8RN4Led1BUDg8akfuXo1F9M2Jnz2dVUukFrNMc0oMmKCglPeQ00N3uvBOuK",
  {
    apiVersion: "2020-08-27",
  }
);

export const Stripe = {
  connect: async (code: string) => {
    const response = await client.oauth.token({
      grant_type: "authorization_code",
      code,
    });

    return response;
  },
  charge: async (amount: number, source: string, stripeAccount: string) => {
    const res = await client.charges.create(
      {
        amount,
        currency: "usd",
        source,
        application_fee_amount: Math.round(amount * 0.05),
      },
      {
        stripeAccount,
      }
    );

    if (res.status !== "succeeded") {
      throw new Error("Failed to create charge with Stripe");
    }
  },
};
